from flask import Flask, render_template, request, jsonify
import sys
import os
import json
import random
import datetime
from collections import defaultdict
sys.path.append('src')
from data_preprocessing import TextPreprocessor
from model import SentimentModel

# Initialize Flask app
app = Flask(__name__)

# Load the preprocessor and model
preprocessor = TextPreprocessor()
model = SentimentModel(model_type='logistic_regression')

# Check if model is already trained
if os.path.exists('models/best_sentiment_model.pkl'):
    model.load_model('models/best_sentiment_model.pkl')
else:
    print("Model not found. Please train the model first using train_model.py.")

# In-memory storage for reviews (in production, use a database)
review_history = []

@app.route('/')
def dashboard():
    """
    Render the dashboard page.
    """
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction based on user input.
    """
    if request.method == 'POST':
        # Get the review text from the form
        review_text = request.form['review_text']
        category = request.form.get('category', 'Other')
        rating = request.form.get('rating', '3')

        # Preprocess the text
        processed_text = preprocessor.preprocess_text(review_text)

        # Make prediction
        prediction = model.predict(processed_text)

        # Convert prediction to sentiment
        sentiment = 'Positive' if prediction == 1 else 'Negative'

        # Generate a confidence score (simulated)
        confidence = round(random.uniform(0.7, 0.95), 2)

        # Save to history
        review_entry = {
            'id': len(review_history) + 1,
            'text': review_text,
            'category': category,
            'rating': rating,
            'sentiment': sentiment,
            'confidence': confidence,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        review_history.append(review_entry)

        # Return the result as JSON
        return jsonify({
            'success': True,
            'sentiment': sentiment,
            'confidence': confidence,
            'review': review_entry
        })

@app.route('/api/history')
def get_history():
    """
    Get review history.
    """
    return jsonify({'reviews': review_history})

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """
    Clear review history.
    """
    global review_history
    review_history = []
    return jsonify({'success': True})

@app.route('/api/metrics')
def get_metrics():
    """
    Get dashboard metrics.
    """
    if not review_history:
        return jsonify({
            'total_reviews': 0,
            'positive_percent': 0,
            'negative_percent': 0,
            'categories': {},
            'sentiments': {'Positive': 0, 'Negative': 0}
        })

    total_reviews = len(review_history)
    positive_count = sum(1 for r in review_history if r['sentiment'] == 'Positive')
    negative_count = total_reviews - positive_count

    positive_percent = round((positive_count / total_reviews) * 100, 1) if total_reviews > 0 else 0
    negative_percent = round((negative_count / total_reviews) * 100, 1) if total_reviews > 0 else 0

    # Count by category
    categories = defaultdict(int)
    for review in review_history:
        categories[review['category']] += 1

    return jsonify({
        'total_reviews': total_reviews,
        'positive_percent': positive_percent,
        'negative_percent': negative_percent,
        'categories': dict(categories),
        'sentiments': {'Positive': positive_count, 'Negative': negative_count}
    })

@app.route('/index')
def index():
    """
    Render the original index page (for backward compatibility).
    """
    return render_template('index.html')

@app.route('/result')
def result():
    """
    Render the result page (for backward compatibility).
    """
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
