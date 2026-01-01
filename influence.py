import pandas as pd
import networkx as nx

# 1. Load your existing sentiment results
df = pd.read_csv("collected_data/youtube_sentiment_results.csv")

# 2. Reconstruct the graph (as per your existing logic)
G = nx.DiGraph()
for _, row in df.iterrows():
    commenter = row["author"]
    video = f"{row['video_title']} ({row['video_id'][:6]})"
    G.add_node(commenter, type='author')
    G.add_node(video, type='video')
    
    if G.has_edge(commenter, video):
        G[commenter][video]['weight'] += 1
    else:
        G.add_edge(commenter, video, weight=1, sentiment=row['sentiment'])

# 3. Calculate Influence Metrics
print("Calculating influence scores...")

# Degree Centrality: Who is the most active/connected?
degree_cent = nx.degree_centrality(G)

# Eigenvector Centrality: Who is connected to the most important videos?
# (Note: Use max_iter=1000 to ensure convergence on larger datasets)
eigen_cent = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)

# Betweenness Centrality: Who acts as a bridge between different video topics?
between_cent = nx.betweenness_centrality(G)

# 4. Aggregate Sentiment by Author
# This creates a "Sentiment Profile" for each consumer
author_sentiment = df.groupby('author').agg({
    'sentiment_score': 'mean',
    'sentiment': lambda x: x.value_counts().index[0] # Most frequent label
}).reset_index()

# 5. Combine Network and Sentiment Data
influence_df = pd.DataFrame({
    'author': [n for n in G.nodes() if G.nodes[n]['type'] == 'author']
})

influence_df['degree_influence'] = influence_df['author'].map(degree_cent)
influence_df['prestige_influence'] = influence_df['author'].map(eigen_cent)
influence_df['bridge_score'] = influence_df['author'].map(between_cent)

# Merge with the sentiment profile
final_analysis = pd.merge(influence_df, author_sentiment, on='author', how='inner')

# Sort by Influence to see the top "Opinion Leaders"
final_analysis = final_analysis.sort_values(by='prestige_influence', ascending=False)

# Save for your project report
final_analysis.to_csv("collected_data/author_influence_profile.csv", index=False)
print("✅ Influence profiles saved to: collected_data/author_influence_profile.csv")
print(final_analysis.head(10))


import matplotlib.pyplot as plt
import seaborn as sns

# Create the visualization
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=final_analysis, 
    x='prestige_influence', 
    y='sentiment_score', 
    size='degree_influence', 
    hue='sentiment',
    palette={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'},
    alpha=0.6
)

plt.title('Consumer Influence vs. Emotional Sentiment')
plt.xlabel('Influence Score (Prestige)')
plt.ylabel('Average Sentiment Score (-1 to 1)')
plt.axhline(0.05, color='gray', linestyle='--', alpha=0.3)
plt.axhline(-0.05, color='gray', linestyle='--', alpha=0.3)                                        
plt.legend(title='Sentiment Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("collected_data/influence_sentiment_matrix.png")
plt.show()

print("✅ Behavioral matrix saved as: collected_data/influence_sentiment_matrix.png")


# In your plotting script (at the bottom of influence.py)

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=final_analysis, 
    x='degree_influence',  # <--- CHANGED from 'prestige_influence'
    y='sentiment_score', 
    size='degree_influence', 
    hue='sentiment',
    palette={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'},
    alpha=0.6
)

plt.title('Consumer Activity vs. Emotional Sentiment') # Updated Title
plt.xlabel('Activity Level (Degree Centrality)') # Updated Label
# ... rest of the code remains the same