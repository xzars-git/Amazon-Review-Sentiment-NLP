from flask import Flask, render_template, request, jsonify, redirect, url_for
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

# Routes
@app.route('/')
def dashboard():
    """
    Render the dashboard page.
    """
    return render_template('dashboard.html')

@app.route('/analyze')
def analyze():
    """
    Render the analyze page.
    """
    return render_template('analyze.html')

@app.route('/history')
def history():
    """
    Render the history page.
    """
    return render_template('history.html')

@app.route('/model')
def model_info():
    """
    Render the model info page.
    """
    return render_template('model.html')

@app.route('/insights')
def insights():
    """
    Render the insights page.
    """
    return render_template('insights.html')

@app.route('/insights/data')
def insights_data():
    """
    Get insights data for charts.
    """
    return jsonify({
        'success': True,
        'insights': {
            'trend_data': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'positive': [65, 68, 66, 70, 68, 72],
                'negative': [35, 32, 34, 30, 32, 28]
            },
            'category_data': {
                'labels': ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports', 'Toys'],
                'positive': [72, 68, 65, 70, 58, 75],
                'negative': [28, 32, 35, 30, 42, 25]
            }
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction based on user input.
    """
    try:
        if request.method == 'POST':
            # Get the review text from the form
            if 'review_text' not in request.form:
                return jsonify({
                    'success': False,
                    'error': 'Missing review_text field'
                }), 400

            review_text = request.form['review_text']
            category = request.form.get('category', 'Other')
            rating = request.form.get('rating', '3')

            if not review_text.strip():
                return jsonify({
                    'success': False,
                    'error': 'Review text cannot be empty'
                }), 400

            # Preprocess the text
            processed_text = preprocessor.preprocess_text(review_text)

            # Make prediction
            try:
                prediction = model.predict(processed_text)
                print(f"Raw prediction: {prediction}")  # Debug line

                # Convert prediction to sentiment
                sentiment = 'Positive' if prediction == 1 else 'Negative'
                print(f"Converted sentiment: {sentiment}")  # Debug line

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
                result = {
                    'success': True,
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'review': review_entry,
                    'sentiment_text': sentiment  # Explicitly add sentiment_text for frontend
                }
                print(f"Result to return: {result}")  # Debug line

                # Ensure all required fields are present
                if not result.get('sentiment_text'):
                    result['sentiment_text'] = sentiment
                if not result.get('sentiment'):
                    result['sentiment'] = sentiment

                return jsonify(result)
            except Exception as e:
                print(f"Error in prediction: {str(e)}")  # Debug line
                return jsonify({
                    'success': False,
                    'error': f'Prediction error: {str(e)}'
                }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history')
def get_history():
    """
    Get review history as JSON.
    """
    try:
        return jsonify({
            'success': True,
            'history': review_history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a review from history.
    """
    try:
        global review_history
        review_history = [r for r in review_history if r['id'] != review_id]
        return jsonify({
            'success': True,
            'message': 'Review deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/model_info')
def get_model_info():
    """
    Get model information as JSON.
    """
    try:
        # Read model evaluation file
        eval_path = 'models/logistic_regression_evaluation_large.txt'
        model_info = {}

        if os.path.exists(eval_path):
            with open(eval_path, 'r') as f:
                content = f.read()
                # Parse the evaluation file
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('Model:'):
                        model_info['model_type'] = line.split(': ')[1]
                    elif line.startswith('Accuracy:'):
                        model_info['accuracy'] = float(line.split(': ')[1])
                    elif line.startswith('Training samples:'):
                        model_info['training_samples'] = int(line.split(': ')[1])
                    elif line.startswith('Testing samples:'):
                        model_info['testing_samples'] = int(line.split(': ')[1])
                    elif line.startswith('Max features:'):
                        model_info['max_features'] = int(line.split(': ')[1])

        return jsonify({
            'success': True,
            'model_info': model_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/insights')
def get_insights():
    """
    Get sentiment insights as JSON.
    """
    try:
        # Generate mock insights data
        insights = {
            'total_reviews': len(review_history) if review_history else 2400000,
            'positive_percentage': 68,
            'negative_percentage': 32,
            'average_rating': 4.2,
            'trend_data': {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'positive': [65, 68, 66, 70, 68, 72],
                'negative': [35, 32, 34, 30, 32, 28]
            },
            'category_data': {
                'labels': ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports', 'Toys'],
                'positive': [72, 68, 65, 70, 58, 75],
                'negative': [28, 32, 35, 30, 42, 25]
            }
        }

        return jsonify({
            'success': True,
            'insights': insights
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
