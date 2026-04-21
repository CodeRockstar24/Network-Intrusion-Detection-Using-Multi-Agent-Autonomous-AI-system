import pandas as pd

data = pd.read_csv(r"C:\Users\elroy\OneDrive\Desktop\Cybersecurity Project CECS378\data\MachineLearningCVE\cleaned_data.csv")

# Normalize labels
data["Label"] = data["Label"].astype(str)

# Compute thresholds using Benign vs Attack
benign = data[data["Label"] == "Benign"]
attack = data[data["Label"] != "Benign"]

thresholds = {
    "SYN Flag Count": (benign["SYN Flag Count"].mean() + attack["SYN Flag Count"].mean()) / 2,
    "Flow Packets/s": (benign["Flow Packets/s"].mean() + attack["Flow Packets/s"].mean()) / 2,
    "Flow Bytes/s": (benign["Flow Bytes/s"].mean() + attack["Flow Bytes/s"].mean()) / 2
}

def analyze_traffic(input_data, detection_output):

    predicted = detection_output.get("prediction", "Unknown")
    confidence = detection_output.get("confidence", 0)

    score = 0
    reasons = []

    # Rule 1: SYN activity
    if input_data.get("SYN Flag Count", 0) > thresholds["SYN Flag Count"] * 0.7:
        score += 2
        reasons.append("Elevated SYN activity")

    # Rule 2: Packet rate
    if input_data.get("Flow Packets/s", 0) > thresholds["Flow Packets/s"] * 0.7:
        score += 2
        reasons.append("High packet rate")

    # Rule 3: Byte rate
    if input_data.get("Flow Bytes/s", 0) > thresholds["Flow Bytes/s"] * 0.7:
        score += 2
        reasons.append("High data volume")

    # Rule 4: Asymmetry
    if input_data.get("Total Fwd Packets", 0) > 2 * input_data.get("Total Backward Packets", 1):
        score += 1
        reasons.append("Traffic asymmetry")


    if predicted != "Benign":
        score += 2
        reasons.append(f"ML detected {predicted}")

    # Normalize
    risk_score = round(score / 9, 2)

    # Decision logic
    if score >= 6:
        confidence_level = "HIGH"
    elif score >= 3:
        confidence_level = "MEDIUM"
    else:
        confidence_level = "LOW"

    return {
        "attack_type": predicted,
        "risk_score": risk_score,
        "confidence": confidence_level,
        "reason": ", ".join(reasons) if reasons else "No strong indicators"
    }