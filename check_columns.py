
import pandas as pd

# Load the data
try:
    # Load data without header and assign column names
    df = pd.read_csv('data/train.csv', header=None)
    print(f"Dataset shape: {df.shape}")

    # Assign column names
    df.columns = ['Rating', 'Title', 'Text']

    print("Column names in the dataset:")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")

    # Display first few rows
    print("\nFirst few rows of the dataset:")
    print(df.head())

    # Show rating distribution
    print("\nRating distribution:")
    print(df['Rating'].value_counts().sort_index())

except Exception as e:
    print(f"Error loading data: {e}")
