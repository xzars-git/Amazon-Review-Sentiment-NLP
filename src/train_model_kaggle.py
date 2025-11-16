import pandas as pd
import os
import argparse
from data_preprocessing import TextPreprocessor, load_data, create_sentiment_labels
from model import SentimentModel, compare_models
from visualization import plot_sentiment_distribution, plot_rating_distribution, plot_word_cloud, save_figure

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Train sentiment analysis model on Amazon review data')
    parser.add_argument('--data_path', type=str, required=True, help='Path to the CSV data file')
    parser.add_argument('--text_column', type=str, default='Text', help='Name of the text column')
    parser.add_argument('--rating_column', type=str, default='Score', help='Name of the rating column')
    parser.add_argument('--model_type', type=str, default='logistic_regression', 
                        choices=['logistic_regression', 'naive_bayes', 'svm', 'random_forest'],
                        help='Type of model to train')
    parser.add_argument('--output_dir', type=str, default='models', help='Directory to save the trained model')
    parser.add_argument('--compare', action='store_true', help='Compare different model types')
    parser.add_argument('--visualize', action='store_true', help='Generate visualizations')
    parser.add_argument('--sample_size', type=int, default=None, help='Number of samples to use for training (use all if not specified)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load data
    print(f"Loading data from {args.data_path}...")
    df = load_data(args.data_path)
    if df is None:
        print("Failed to load data. Exiting.")
        return
        
    # Sample data if sample_size is specified
    if args.sample_size is not None and args.sample_size < len(df):
        print(f"Sampling {args.sample_size} records from the dataset...")
        df = df.sample(n=args.sample_size, random_state=42)

    # Create sentiment labels
    print("Creating sentiment labels...")
    df_labeled = create_sentiment_labels(df, args.rating_column, args.text_column)

    # Preprocess text
    print("Preprocessing text data...")
    preprocessor = TextPreprocessor()
    df_processed = preprocessor.preprocess_dataframe(df_labeled, args.text_column)

    # Generate visualizations if requested
    if args.visualize:
        print("Generating visualizations...")

        # Create visualizations directory
        viz_dir = os.path.join(args.output_dir, 'visualizations')
        os.makedirs(viz_dir, exist_ok=True)

        # Plot sentiment distribution
        sentiment_fig = plot_sentiment_distribution(df_processed, 'sentiment_binary')
        save_figure(sentiment_fig, os.path.join(viz_dir, 'sentiment_distribution.png'))

        # Plot rating distribution
        rating_fig = plot_rating_distribution(df_labeled, args.rating_column)
        save_figure(rating_fig, os.path.join(viz_dir, 'rating_distribution.png'))

        # Plot word cloud for positive reviews
        positive_text = ' '.join(df_processed[df_processed['sentiment_binary'] == 1][f'{args.text_column}_processed'])
        positive_wordcloud = plot_word_cloud(positive_text, "Word Cloud of Positive Reviews")
        save_figure(positive_wordcloud, os.path.join(viz_dir, 'positive_wordcloud.png'))

        # Plot word cloud for negative reviews
        negative_text = ' '.join(df_processed[df_processed['sentiment_binary'] == 0][f'{args.text_column}_processed'])
        negative_wordcloud = plot_word_cloud(negative_text, "Word Cloud of Negative Reviews")
        save_figure(negative_wordcloud, os.path.join(viz_dir, 'negative_wordcloud.png'))

    # Compare models if requested
    if args.compare:
        print("Comparing different models...")
        results = compare_models(df_processed, f'{args.text_column}_processed', 'sentiment_binary')

        # Save comparison results
        comparison_file = os.path.join(args.output_dir, 'model_comparison.txt')
        with open(comparison_file, 'w') as f:
            for model_type, metrics in results.items():
                f.write(f"Model: {model_type}\n")
                f.write(f"Accuracy: {metrics['accuracy']:.4f}\n")
                f.write(f"Classification Report:\n{metrics['classification_report']}\n")
                f.write(f"Confusion Matrix:\n{metrics['confusion_matrix']}\n\n")

        print(f"Model comparison results saved to {comparison_file}")

    # Train the specified model
    print(f"Training {args.model_type} model...")
    model = SentimentModel(model_type=args.model_type)
    X_train, X_test, y_train, y_test = model.prepare_data(
        df_processed, f'{args.text_column}_processed', 'sentiment_binary'
    )
    model.train(X_train, y_train)

    # Evaluate the model
    print("Evaluating model...")
    results = model.evaluate(X_test, y_test)

    # Save the model
    model_path = os.path.join(args.output_dir, f'{args.model_type}_model.pkl')
    model.save_model(model_path)

    # Also save as best_sentiment_model.pkl for the web app
    best_model_path = os.path.join(args.output_dir, 'best_sentiment_model.pkl')
    model.save_model(best_model_path)

    # Save evaluation results
    eval_file = os.path.join(args.output_dir, f'{args.model_type}_evaluation.txt')
    with open(eval_file, 'w') as f:
        f.write(f"Model: {args.model_type}\n")
        f.write(f"Accuracy: {results['accuracy']:.4f}\n")
        f.write(f"Classification Report:\n{results['classification_report']}\n")
        f.write(f"Confusion Matrix:\n{results['confusion_matrix']}\n")

    print(f"Model evaluation results saved to {eval_file}")
    print("Training completed successfully!")

if __name__ == "__main__":
    main()
