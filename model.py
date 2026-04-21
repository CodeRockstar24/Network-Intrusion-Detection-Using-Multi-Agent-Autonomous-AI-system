import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Load data
data = pd.read_csv(r"C:\Users\elroy\OneDrive\Desktop\Cybersecurity Project CECS378\data\MachineLearningCVE\cleaned_data.csv")

# Sample 200k rows
data = data.sample(n=200000, random_state=42)

# Reduce memory usage
data = data.astype("float32", errors="ignore")

print("Loaded data:", data.shape)

# Split features and label
X = data.drop("Label", axis=1)
y = data["Label"]

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Train model
model = RandomForestClassifier(
    n_estimators=50,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Predictions
predictions = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, predictions))
print("Report:\n", classification_report(y_test, predictions, target_names=le.classes_))

# Save model + encoder
joblib.dump(model, r"C:\Users\elroy\OneDrive\Desktop\Cybersecurity Project CECS378\models\model.pkl")
joblib.dump(le, r"C:\Users\elroy\OneDrive\Desktop\Cybersecurity Project CECS378\models\label_encoder.pkl")

print("Model and encoder saved.")