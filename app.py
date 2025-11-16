from flask import Flask, render_template, request
import sys
import os
sys.path.append('src')
from data_preprocessing import TextPreprocessor
from model import SentimentModel

# Initialize Flask app
app = Flask(__name__)

# Load the preprocessor and model
preprocessor = TextPreprocessor()
model = SentimentModel(model_type='logistic_regression')

# Check if model is already trained
if os.path.exists('models/logistic_regression_model.pkl'):
    model.load_model('models/logistic_regression_model.pkl')
else:
    print("Model not found. Please train the model first using train_model.py.")

@app.route('/')
def home():
    """
    Render the home page.
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction based on user input.
    """
    if request.method == 'POST':
        # Get the review text from the form
        review_text = request.form['review_text']

        # Preprocess the text
        processed_text = preprocessor.preprocess_text(review_text)

        # Make prediction
        prediction = model.predict(processed_text)

        # Convert prediction to sentiment
        sentiment = 'Positive' if prediction == 1 else 'Negative'

        # Return the result
        return render_template('result.html', 
                              original_text=review_text, 
                              sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
