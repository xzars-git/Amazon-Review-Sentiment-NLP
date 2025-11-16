
import pandas as pd
import os
import argparse
from data_preprocessing import TextPreprocessor, load_data, create_sentiment_labels
from model import SentimentModel
from visualization import plot_sentiment_distribution, plot_rating_distribution, plot_word_cloud, save_figure
import time

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Train sentiment analysis model on Amazon review data')
    parser.add_argument('--data_path', type=str, required=True, help='Path to the CSV data file')
    parser.add_argument('--text_column', type=str, default='Text', help='Name of the text column')
    parser.add_argument('--rating_column', type=str, default='Rating', help='Name of the rating column')
    parser.add_argument('--model_type', type=str, default='logistic_regression',
                        choices=['logistic_regression', 'naive_bayes'],
                        help='Type of model to train')
    parser.add_argument('--output_dir', type=str, default='models', help='Directory to save the trained model')
    parser.add_argument('--visualize', action='store_true', help='Generate visualizations')
    parser.add_argument('--max_samples', type=int, default=1000000, help='Maximum number of samples to use')
    parser.add_argument('--batch_size', type=int, default=100000, help='Batch size for processing data')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"Loading data from {args.data_path}...")

    # Load data in chunks to handle large datasets
    chunks = []
    for chunk in pd.read_csv(args.data_path, header=None, chunksize=args.batch_size):
        chunk.columns = ['Rating', 'Title', 'Text']
        chunks.append(chunk)

        # Stop if we've reached max_samples
        total_rows = sum(len(c) for c in chunks)
        if total_rows >= args.max_samples:
            # Trim the last chunk if needed
            if total_rows > args.max_samples:
                chunks[-1] = chunks[-1].iloc[:args.max_samples - (total_rows - len(chunks[-1]))]
            break

    # Concatenate all chunks
    df = pd.concat(chunks, ignore_index=True)
    print(f"Loaded {len(df)} records")

    # Create sentiment labels
    print("Creating sentiment labels...")
    df_labeled = create_sentiment_labels(df, args.rating_column, args.text_column)

    # Preprocess text
    print("Preprocessing text data...")
    preprocessor = TextPreprocessor()

    # Process in batches to avoid memory issues
    processed_chunks = []
    for i in range(0, len(df_labeled), args.batch_size):
        batch = df_labeled.iloc[i:i+args.batch_size].copy()
        processed_batch = preprocessor.preprocess_dataframe(batch, args.text_column)
        processed_chunks.append(processed_batch)
        print(f"Processed {min(i+args.batch_size, len(df_labeled))} of {len(df_labeled)} records")

    df_processed = pd.concat(processed_chunks, ignore_index=True)

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

    # Train the specified model
    print(f"Training {args.model_type} model...")
    model = SentimentModel(model_type=args.model_type)
    X_train, X_test, y_train, y_test = model.prepare_data(
        df_processed, f'{args.text_column}_processed', 'sentiment_binary'
    )

    print(f"Training on {len(X_train)} samples...")
    start_time = time.time()
    model.train(X_train, y_train)
    training_time = time.time() - start_time
    print(f"Training completed in {training_time:.2f} seconds")

    # Evaluate the model
    print("Evaluating model...")
    metrics = model.evaluate(X_test, y_test)

    # Print evaluation results
    print(f"Model: {args.model_type}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print("Classification Report:")
    print(metrics['classification_report'])
    print("Confusion Matrix:")
    print(metrics['confusion_matrix'])

    # Save the model
    model_path = os.path.join(args.output_dir, f'{args.model_type}_model.pkl')
    model.save_model(model_path)

    # Also save as best_sentiment_model.pkl for compatibility with the app
    best_model_path = os.path.join(args.output_dir, 'best_sentiment_model.pkl')
    model.save_model(best_model_path)

    # Save evaluation results
    eval_path = os.path.join(args.output_dir, f'{args.model_type}_evaluation.txt')
    with open(eval_path, 'w') as f:
        f.write(f"Model: {args.model_type}
")
        f.write(f"Training samples: {len(X_train)}
")
        f.write(f"Testing samples: {len(X_test)}
")
        f.write(f"Training time: {training_time:.2f} seconds
")
        f.write(f"Accuracy: {metrics['accuracy']:.4f}
")
        f.write("Classification Report:
")
        f.write(metrics['classification_report'])
        f.write("
Confusion Matrix:
")
        f.write(str(metrics['confusion_matrix']))

    print(f"Model saved to {model_path}")
    print(f"Evaluation results saved to {eval_path}")
    print("Training completed successfully!")

if __name__ == "__main__":
    main()
