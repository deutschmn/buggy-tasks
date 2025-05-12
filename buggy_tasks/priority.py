import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import joblib
import os

# Path to the reference data
REFERENCE_DATA_PATH = os.path.join(
    os.path.dirname(__file__), '../data/reference.json')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'priority_model.pkl')


def train_priority_model():
    """Train the SVC model using the data in reference.json."""
    print("Training the priority model...")

    # Load the reference data
    with open(REFERENCE_DATA_PATH, 'r') as f:
        data = json.load(f)

    print(f"Loaded reference data. Number of items: {len(data)}")

    # Extract tags and priorities
    texts = [" ".join(item['tags']) for item in data]
    priorities = [item['priority'] for item in data]

    # Create a pipeline with TfidfVectorizer and SVC
    model = make_pipeline(TfidfVectorizer(), SVC())

    # Train the model
    print("Fitting the model...")
    model.fit(texts, priorities)

    # Save the trained model
    print(f"Saving the model to {MODEL_PATH}...")
    joblib.dump(model, MODEL_PATH)
    print("Model saved successfully.")


def compute_priority(tags) -> int:
    """Predict the priority of a TODO based on its tags."""
    # Ensure the model is trained
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found. Please train the model first.")

    # Load the trained model
    model = joblib.load(MODEL_PATH)

    # Predict the priority
    tags_text = " ".join(tags)
    print(f"Predicting priority for tags: {tags_text}")
    priority = model.predict([tags_text])[0].item()
    print(f"Predicted priority: {priority}")
    return priority
