
from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR, "models", "fraud_detection_model.pkl"
)

DATA_PATH = os.path.join(
    BASE_DIR, "data", "transactions.csv"
)

ENGINEERED_DATA_PATH = os.path.join(
    BASE_DIR, "data", "transactions_engineered.csv"
)

# Load trained ML model
model = joblib.load(MODEL_PATH)


@app.route("/")
def home():
    return render_template("index.html")


# DASHBOARD API
@app.route("/api/dashboard")
def dashboard():
    try:
        data = pd.read_csv(DATA_PATH)

        total = len(data)
        fraud = int(data["is_fraud"].sum())
        normal = total - fraud

        return jsonify({
            "total_transactions": total,
            "fraud_transactions": fraud,
            "normal_transactions": normal,
            "fraud_rate": round(
                (fraud / total * 100) if total else 0, 2
            )
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# TRANSACTION PREDICTION API
@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        details = request.get_json()

        amount = float(details["amount"])
        hour = int(details["hour"])
        international = int(details["international"])
        location_mismatch = int(details["location_mismatch"])
        card_present = int(details["card_present"])
        transactions = int(details["transactions_last_24h"])

        if amount < 0 or not 0 <= hour <= 23 or transactions < 0:
            return jsonify({
                "error": "Invalid transaction values"
            }), 400

        input_data = pd.DataFrame([{
            "amount": amount,
            "hour": hour,
            "international": international,
            "location_mismatch": location_mismatch,
            "card_present": card_present,
            "transactions_last_24h": transactions,
            "high_amount": int(amount > 35000),
            "night_transaction": int(0 <= hour < 4),
            "high_frequency": int(transactions > 10),
            "international_mismatch": (
                international * location_mismatch
            ),
            "amount_per_transaction": amount / (transactions + 1)
        }])

        input_data = input_data[
            list(model.feature_names_in_)
        ]

        prediction = int(model.predict(input_data)[0])

        probability = float(
            model.predict_proba(input_data)[0][1]
        )

        risk_score = probability * 100

        if risk_score < 30:
            risk_level = "Low Risk"
        elif risk_score < 70:
            risk_level = "Medium Risk"
        else:
            risk_level = "High Risk"

        return jsonify({
            "prediction": "Fraud" if prediction == 1 else "Normal",
            "fraud_probability": round(probability * 100, 2),
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


# CONFUSION MATRIX API
@app.route("/api/confusion-matrix")
def confusion_matrix_data():
    try:
        data = pd.read_csv(ENGINEERED_DATA_PATH)

        X = data.drop(
            columns=["transaction_id", "is_fraud"]
        )
        y = data["is_fraud"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        X_test = X_test[
            list(model.feature_names_in_)
        ]

        predictions = model.predict(X_test)

        matrix = confusion_matrix(
            y_test,
            predictions,
            labels=[0, 1]
        )

        return jsonify({
            "labels": ["Normal", "Fraud"],
            "matrix": matrix.tolist(),
            "true_normal": int(matrix[0][0]),
            "false_fraud": int(matrix[0][1]),
            "missed_fraud": int(matrix[1][0]),
            "true_fraud": int(matrix[1][1]),
            "status": "success"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
