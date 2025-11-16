import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

class SentimentModel:
    """
    A class for building, training, and evaluating sentiment analysis models.
    """

    def __init__(self, model_type='logistic_regression'):
        """
        Initialize the sentiment model.

        Parameters:
        model_type (str): Type of model to use. Options: 'logistic_regression', 'naive_bayes', 'svm', 'random_forest'
        """
        self.model_type = model_type
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = self._initialize_model()
        self.is_trained = False

    def _initialize_model(self):
        """
        Initialize the model based on model_type.

        Returns:
        sklearn model: Initialized model
        """
        if self.model_type == 'logistic_regression':
            return LogisticRegression(random_state=42)
        elif self.model_type == 'naive_bayes':
            return MultinomialNB()
        elif self.model_type == 'svm':
            return SVC(kernel='linear', random_state=42)
        elif self.model_type == 'random_forest':
            return RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")

    def prepare_data(self, df, text_column, sentiment_column):
        """
        Prepare data for training and testing.

        Parameters:
        df (pandas.DataFrame): Input dataframe
        text_column (str): Name of the column containing text
        sentiment_column (str): Name of the column containing sentiment labels

        Returns:
        tuple: X_train, X_test, y_train, y_test
        """
        # Extract features and target
        X = df[text_column]
        y = df[sentiment_column]

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train):
        """
        Train the sentiment model.

        Parameters:
        X_train (pandas.Series): Training text data
        y_train (pandas.Series): Training sentiment labels
        """
        # Vectorize text data
        X_train_vectorized = self.vectorizer.fit_transform(X_train)

        # Train the model
        self.model.fit(X_train_vectorized, y_train)
        self.is_trained = True

        print(f"Model ({self.model_type}) trained successfully!")

    def evaluate(self, X_test, y_test):
        """
        Evaluate the sentiment model.

        Parameters:
        X_test (pandas.Series): Testing text data
        y_test (pandas.Series): Testing sentiment labels

        Returns:
        dict: Dictionary containing evaluation metrics
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet. Call train() first.")

        # Vectorize test data
        X_test_vectorized = self.vectorizer.transform(X_test)

        # Make predictions
        y_pred = self.model.predict(X_test_vectorized)

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)

        print(f"Model: {self.model_type}")
        print(f"Accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(report)
        print("Confusion Matrix:")
        print(cm)

        return {
            'accuracy': accuracy,
            'classification_report': report,
            'confusion_matrix': cm
        }

    def predict(self, text):
        """
        Predict sentiment for a single text.

        Parameters:
        text (str): Input text

        Returns:
        int: Predicted sentiment (0 for negative, 1 for positive)
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet. Call train() first.")

        # Vectorize text
        text_vectorized = self.vectorizer.transform([text])

        # Make prediction
        prediction = self.model.predict(text_vectorized)[0]

        return prediction

    def save_model(self, model_path):
        """
        Save the trained model and vectorizer.

        Parameters:
        model_path (str): Path to save the model
        """
        if not self.is_trained:
            raise ValueError("Model is not trained yet. Call train() first.")

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        # Save model and vectorizer
        model_data = {
            'model': self.model,
            'vectorizer': self.vectorizer,
            'model_type': self.model_type
        }

        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)

        print(f"Model saved to {model_path}")

    def load_model(self, model_path):
        """
        Load a trained model and vectorizer.

        Parameters:
        model_path (str): Path to the saved model
        """
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)

        self.model = model_data['model']
        self.vectorizer = model_data['vectorizer']
        self.model_type = model_data['model_type']
        self.is_trained = True

        print(f"Model loaded from {model_path}")

def compare_models(df, text_column, sentiment_column):
    """
    Compare different sentiment analysis models.

    Parameters:
    df (pandas.DataFrame): Input dataframe
    text_column (str): Name of the column containing text
    sentiment_column (str): Name of the column containing sentiment labels

    Returns:
    dict: Dictionary containing evaluation results for each model
    """
    model_types = ['logistic_regression', 'naive_bayes', 'svm', 'random_forest']
    results = {}

    # Prepare data
    X_train, X_test, y_train, y_test = train_test_split(
        df[text_column], df[sentiment_column], test_size=0.2, random_state=42, stratify=df[sentiment_column]
    )

    for model_type in model_types:
        print(f"Training and evaluating {model_type} model...")
        model = SentimentModel(model_type=model_type)
        model.train(X_train, y_train)
        results[model_type] = model.evaluate(X_test, y_test)

    return results

if __name__ == "__main__":
    # Example usage
    # Create a sample dataframe
    data = {
        'text': [
            "This product is amazing! I love it.",
            "Terrible product. Waste of money.",
            "It's okay, not great but not terrible either.",
            "I would definitely recommend this to others.",
            "Poor quality, broke after a week."
        ],
        'sentiment': [1, 0, 1, 1, 0]
    }
    df = pd.DataFrame(data)

    # Train a model
    model = SentimentModel(model_type='logistic_regression')
    X_train, X_test, y_train, y_test = model.prepare_data(df, 'text', 'sentiment')
    model.train(X_train, y_train)
    model.evaluate(X_test, y_test)

    # Make a prediction
    test_text = "This is the best product I've ever bought!"
    prediction = model.predict(test_text)
    sentiment = "positive" if prediction == 1 else "negative"
    print(f"Text: '{test_text}'")
    print(f"Predicted sentiment: {sentiment}")
