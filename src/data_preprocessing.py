import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download NLTK resources if needed
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class TextPreprocessor:
    """
    A class for preprocessing text data for sentiment analysis.
    """

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        """
        Clean text by removing special characters, numbers, and converting to lowercase.

        Parameters:
        text (str): Input text to clean

        Returns:
        str: Cleaned text
        """
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)

        # Remove non-alphabetic characters and convert to lowercase
        text = re.sub(r'[^a-zA-Z]', ' ', text).lower()

        return text

    def tokenize_and_remove_stopwords(self, text):
        """
        Tokenize text and remove stopwords.

        Parameters:
        text (str): Input text to tokenize

        Returns:
        list: List of tokens without stopwords
        """
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words]
        return tokens

    def lemmatize_tokens(self, tokens):
        """
        Lemmatize tokens to their base form.

        Parameters:
        tokens (list): List of tokens to lemmatize

        Returns:
        list: List of lemmatized tokens
        """
        lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return lemmatized_tokens

    def preprocess_text(self, text):
        """
        Complete preprocessing pipeline for text.

        Parameters:
        text (str): Input text to preprocess

        Returns:
        str: Preprocessed text
        """
        # Clean text
        cleaned_text = self.clean_text(text)

        # Tokenize and remove stopwords
        tokens = self.tokenize_and_remove_stopwords(cleaned_text)

        # Lemmatize tokens
        lemmatized_tokens = self.lemmatize_tokens(tokens)

        # Join tokens back into text
        preprocessed_text = ' '.join(lemmatized_tokens)

        return preprocessed_text

    def preprocess_dataframe(self, df, text_column):
        """
        Apply preprocessing to a dataframe column.

        Parameters:
        df (pandas.DataFrame): Input dataframe
        text_column (str): Name of the column containing text to preprocess

        Returns:
        pandas.DataFrame: Dataframe with preprocessed text
        """
        df_copy = df.copy()
        df_copy[f'{text_column}_processed'] = df_copy[text_column].apply(self.preprocess_text)
        return df_copy

def load_data(file_path):
    """
    Load data from a CSV file.

    Parameters:
    file_path (str): Path to the CSV file

    Returns:
    pandas.DataFrame: Loaded dataframe
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def create_sentiment_labels(df, rating_column, text_column):
    """
    Create sentiment labels based on ratings.

    Parameters:
    df (pandas.DataFrame): Input dataframe
    rating_column (str): Name of the column containing ratings
    text_column (str): Name of the column containing text

    Returns:
    pandas.DataFrame: Dataframe with sentiment labels
    """
    df_copy = df.copy()

    # Create sentiment labels based on rating
    # 1-2 stars: Negative, 3 stars: Neutral, 4-5 stars: Positive
    df_copy['sentiment'] = df_copy[rating_column].apply(
        lambda x: 'negative' if x <= 2 else ('neutral' if x == 3 else 'positive')
    )

    # Filter out neutral reviews for binary classification
    df_binary = df_copy[df_copy['sentiment'] != 'neutral'].copy()

    # Convert sentiment to binary (0 for negative, 1 for positive)
    df_binary['sentiment_binary'] = df_binary['sentiment'].apply(
        lambda x: 0 if x == 'negative' else 1
    )

    return df_binary

if __name__ == "__main__":
    # Example usage
    preprocessor = TextPreprocessor()

    # Example text
    example_text = "This product is amazing! I would definitely buy it again."

    # Preprocess the text
    preprocessed_text = preprocessor.preprocess_text(example_text)
    print(f"Original text: {example_text}")
    print(f"Preprocessed text: {preprocessed_text}")
