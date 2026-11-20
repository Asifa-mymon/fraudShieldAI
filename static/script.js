document.addEventListener("DOMContentLoaded", function () {

    // PAGE NAVIGATION
    function showPage(pageId) {
        document.querySelectorAll(".page").forEach(page => {
            page.classList.remove("active");
        });

        document.querySelectorAll(".nav-link").forEach(button => {
            button.classList.remove("active");
        });

        const selectedPage = document.getElementById(pageId);

        if (selectedPage) {
            selectedPage.classList.add("active");
        }

        const selectedButton = document.querySelector(
            `.nav-link[data-page="${pageId}"]`
        );

        if (selectedButton) {
            selectedButton.classList.add("active");
        }

        const heading = document.getElementById("page-heading");

        const titles = {
            dashboard: "Dashboard",
            analysis: "Transaction Analysis",
            performance: "Model Performance",
            about: "About Project"
        };

        if (heading) {
            heading.textContent = titles[pageId] || "Dashboard";
        }
    }

    // Make navigation available to HTML buttons
    window.showPage = showPage;

    document.querySelectorAll(".nav-link").forEach(button => {
        button.addEventListener("click", function () {
            showPage(this.dataset.page);
        });
    });


    // LOAD DASHBOARD STATISTICS
    async function loadDashboard() {
        try {
            const response = await fetch("/api/dashboard");
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Dashboard loading failed");
            }

            document.getElementById("total-transactions").textContent =
                data.total_transactions ?? 0;

            document.getElementById("fraud-transactions").textContent =
                data.fraud_transactions ?? 0;

            document.getElementById("normal-transactions").textContent =
                data.normal_transactions ?? 0;

            document.getElementById("fraud-rate").textContent =
                (data.fraud_rate ?? 0) + "%";

        } catch (error) {
            console.error("Dashboard Error:", error);
        }
    }

    loadDashboard();


    // TRANSACTION ANALYSIS
    const form = document.getElementById("transaction-form");

    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        const result = document.getElementById("result");
        const button = document.getElementById("analyze-btn");

        button.disabled = true;
        button.textContent = "Analyzing...";

        result.hidden = false;
        result.textContent = "Analyzing transaction...";

        const transaction = {
            amount: Number(document.getElementById("amount").value),
            hour: Number(document.getElementById("hour").value),

            international:
                Number(document.getElementById("international").value),

            location_mismatch:
                Number(document.getElementById("location_mismatch").value),

            card_present:
                Number(document.getElementById("card_present").value),

            transactions_last_24h:
                Number(document.getElementById("transactions_last_24h").value)
        };

        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(transaction)
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Prediction failed");
            }

            let riskClass = "risk-low";

            if (data.risk_level === "High") {
                riskClass = "risk-high";
            } else if (data.risk_level === "Medium") {
                riskClass = "risk-medium";
            }

            const prediction = document.createElement("h3");
            prediction.textContent =
                "Prediction: " + data.prediction;

            const probability = document.createElement("p");
            probability.textContent =
                "Fraud Probability: " +
                Number(data.fraud_probability).toFixed(2) + "%";

            const score = document.createElement("p");
            score.textContent =
                "Risk Score: " +
                Number(data.risk_score).toFixed(2) + "%";

            const level = document.createElement("p");
            level.className = riskClass;
            level.textContent =
                "Risk Level: " + data.risk_level;

            const card = document.createElement("div");
            card.className = "result-card";

            card.append(prediction, probability, score, level);

            result.replaceChildren(card);

        } catch (error) {
            result.textContent = "Error: " + error.message;
        }

        button.disabled = false;
        button.textContent = "Analyze Transaction";

    });

});