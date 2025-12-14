import pandas as pd
import glob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()

def get_sentiment_score(text):
    return analyzer.polarity_scores(str(text))["compound"]

def get_sentiment_label(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def load_all_youtube_comments():
    files = glob.glob("collected_data/youtube_*.csv")
    if not files:
        raise FileNotFoundError("No YouTube CSV files found in collected_data/")

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df["source_file"] = f
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)

def main():
    df = load_all_youtube_comments()

    if "text" not in df.columns:
        raise KeyError("Expected column 'text' not found in dataset")

    print(f"Loaded {len(df):,} YouTube comments")

    # Sentiment analysis
    df["sentiment_score"] = df["text"].apply(get_sentiment_score)
    df["sentiment"] = df["sentiment_score"].apply(get_sentiment_label)

    # Save results
    output_file = "collected_data/youtube_sentiment_results.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")

    print("\nSentiment distribution:")
    print(df["sentiment"].value_counts())

    print(f"\n✅ Sentiment results saved to: {output_file}")

if __name__ == "__main__":
    main()
