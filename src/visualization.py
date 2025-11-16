import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np
from collections import Counter

# Set style for plots
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def plot_sentiment_distribution(df, sentiment_column):
    """
    Plot the distribution of sentiments in the dataset.

    Parameters:
    df (pandas.DataFrame): Input dataframe
    sentiment_column (str): Name of the column containing sentiment labels

    Returns:
    matplotlib.figure.Figure: The generated figure
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Count sentiment values
    sentiment_counts = df[sentiment_column].value_counts()

    # Create bar plot
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)

    # Set labels and title
    ax.set_title('Distribution of Sentiments', fontsize=16)
    ax.set_xlabel('Sentiment', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)

    # Add count labels on bars
    for i, count in enumerate(sentiment_counts.values):
        ax.text(i, count + 0.1 * max(sentiment_counts.values), str(count), 
                ha='center', fontsize=12)

    plt.tight_layout()
    return fig

def plot_rating_distribution(df, rating_column):
    """
    Plot the distribution of ratings in the dataset.

    Parameters:
    df (pandas.DataFrame): Input dataframe
    rating_column (str): Name of the column containing ratings

    Returns:
    matplotlib.figure.Figure: The generated figure
    """
    fig, ax = plt.subplots(figsize=(8, 6))

    # Count rating values
    rating_counts = df[rating_column].value_counts().sort_index()

    # Create bar plot
    sns.barplot(x=rating_counts.index, y=rating_counts.values, ax=ax)

    # Set labels and title
    ax.set_title('Distribution of Ratings', fontsize=16)
    ax.set_xlabel('Rating', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)

    # Add count labels on bars
    for i, count in enumerate(rating_counts.values):
        ax.text(i, count + 0.1 * max(rating_counts.values), str(count), 
                ha='center', fontsize=12)

    plt.tight_layout()
    return fig

def plot_word_cloud(text, title="Word Cloud"):
    """
    Generate and display a word cloud from the input text.

    Parameters:
    text (str): Input text
    title (str): Title for the word cloud

    Returns:
    matplotlib.figure.Figure: The generated figure
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Generate word cloud
    wordcloud = WordCloud(width=800, height=600, background_color='white',
                          max_words=100, contour_width=3, 
                          contour_color='steelblue').generate(text)

    # Display the word cloud
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(title, fontsize=16)

    plt.tight_layout()
    return fig

def plot_most_common_words(texts, n=20, title="Most Common Words"):
    """
    Plot the most common words in a list of texts.

    Parameters:
    texts (list): List of text strings
    n (int): Number of most common words to display
    title (str): Title for the plot

    Returns:
    matplotlib.figure.Figure: The generated figure
    """
    # Combine all texts
    combined_text = ' '.join(texts)

    # Tokenize and count words
    words = combined_text.split()
    word_counts = Counter(words)

    # Get most common words
    most_common_words = word_counts.most_common(n)

    # Create dataframe for plotting
    df_words = pd.DataFrame(most_common_words, columns=['Word', 'Count'])

    # Create plot
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x='Count', y='Word', data=df_words, ax=ax)

    # Set labels and title
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Count', fontsize=12)
    ax.set_ylabel('Word', fontsize=12)

    plt.tight_layout()
    return fig

def plot_sentiment_by_rating(df, rating_column, sentiment_column):
    """
    Plot sentiment distribution by rating.

    Parameters:
    df (pandas.DataFrame): Input dataframe
    rating_column (str): Name of the column containing ratings
    sentiment_column (str): Name of the column containing sentiment labels

    Returns:
    matplotlib.figure.Figure: The generated figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create a crosstab of rating and sentiment
    rating_sentiment = pd.crosstab(df[rating_column], df[sentiment_column])

    # Normalize to get proportions
    rating_sentiment_prop = rating_sentiment.div(rating_sentiment.sum(axis=1), axis=0)

    # Plot stacked bar chart
    rating_sentiment_prop.plot(kind='bar', stacked=True, ax=ax, 
                               color=['#FF9999', '#66B2FF'])

    # Set labels and title
    ax.set_title('Sentiment Distribution by Rating', fontsize=16)
    ax.set_xlabel('Rating', fontsize=12)
    ax.set_ylabel('Proportion', fontsize=12)
    ax.legend(title='Sentiment', labels=['Negative', 'Positive'])

    plt.tight_layout()
    return fig

def plot_text_length_distribution(df, text_column, sentiment_column):
    """
    Plot the distribution of text lengths by sentiment.

    Parameters:
    df (pandas.DataFrame): Input dataframe
    text_column (str): Name of the column containing text
    sentiment_column (str): Name of the column containing sentiment labels

    Returns:
    matplotlib.figure.Figure: The generated figure
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Calculate text lengths
    df['text_length'] = df[text_column].apply(lambda x: len(str(x).split()))

    # Plot distribution by sentiment
    sns.histplot(data=df, x='text_length', hue=sentiment_column, 
                 kde=True, ax=ax, alpha=0.7)

    # Set labels and title
    ax.set_title('Distribution of Text Length by Sentiment', fontsize=16)
    ax.set_xlabel('Text Length (Number of Words)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.legend(title='Sentiment', labels=['Negative', 'Positive'])

    plt.tight_layout()
    return fig

def save_figure(fig, file_path, dpi=300):
    """
    Save a matplotlib figure to a file.

    Parameters:
    fig (matplotlib.figure.Figure): Figure to save
    file_path (str): Path to save the figure
    dpi (int): Resolution in dots per inch
    """
    fig.savefig(file_path, dpi=dpi, bbox_inches='tight')
    print(f"Figure saved to {file_path}")

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
        'rating': [5, 1, 3, 4, 2],
        'sentiment': [1, 0, 1, 1, 0]
    }
    df = pd.DataFrame(data)

    # Plot sentiment distribution
    sentiment_fig = plot_sentiment_distribution(df, 'sentiment')

    # Plot rating distribution
    rating_fig = plot_rating_distribution(df, 'rating')

    # Plot word cloud for all reviews
    all_text = ' '.join(df['text'])
    wordcloud_fig = plot_word_cloud(all_text, "Word Cloud of Reviews")

    # Plot most common words
    common_words_fig = plot_most_common_words(df['text'], title="Most Common Words in Reviews")

    # Plot sentiment by rating
    sentiment_by_rating_fig = plot_sentiment_by_rating(df, 'rating', 'sentiment')

    # Plot text length distribution
    text_length_fig = plot_text_length_distribution(df, 'text', 'sentiment')

    # Save figures
    save_figure(sentiment_fig, 'sentiment_distribution.png')
    save_figure(rating_fig, 'rating_distribution.png')
    save_figure(wordcloud_fig, 'wordcloud.png')
    save_figure(common_words_fig, 'common_words.png')
    save_figure(sentiment_by_rating_fig, 'sentiment_by_rating.png')
    save_figure(text_length_fig, 'text_length_distribution.png')

    plt.show()
