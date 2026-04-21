import joblib
import pandas as pd

model = joblib.load(r"C:\Users\elroy\OneDrive\Desktop\Cybersecurity Project CECS378\models\model.pkl")
le = joblib.load(r"C:\Users\elroy\OneDrive\Desktop\Cybersecurity Project CECS378\models\label_encoder.pkl")

# Feature list must match training data EXACTLY
feature_order = list(model.feature_names_in_)

def get_risk_level(prob):
    if prob > 0.8:
        return "HIGH"
    elif prob > 0.5:
        return "MEDIUM"
    else:
        return "LOW"

def detect_traffic(input_data):
    try:
        input_df = pd.DataFrame([input_data])

        # Ensure all required features exist
        for feature in feature_order:
            if feature not in input_df:
                input_df[feature] = 0

        # Reorder columns
        input_df = input_df[feature_order]

        # Model prediction
        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]

        predicted_label = le.inverse_transform([prediction])[0]
        confidence = float(max(probabilities))

        # Determine status
        status = "NORMAL" if predicted_label == "Benign" else "ATTACK"

        if predicted_label == "Benign":
            risk = "LOW"
        else:
            risk = get_risk_level(confidence)

        return {
            "status": status,
            "prediction": predicted_label,
            "confidence": round(confidence, 3),
            "risk_level": risk
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }