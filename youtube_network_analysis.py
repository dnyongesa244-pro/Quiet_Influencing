import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load sentiment results
df = pd.read_csv("collected_data/youtube_sentiment_results.csv")

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for _, row in df.iterrows():
    commenter = row["author"]
    video = f"{row['video_title']} ({row['video_id'][:6]})"  # shorter label
    
    # Add nodes
    G.add_node(commenter, type='author')
    G.add_node(video, type='video')
    
    # Add edge or increase weight if exists
    if G.has_edge(commenter, video):
        G[commenter][video]['weight'] += 1
    else:
        G.add_edge(commenter, video, weight=1, sentiment=row['sentiment'])

# Basic stats
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

# Draw a small subgraph for visualization
# Pick top 20 commenters with most comments
top_commenters = df['author'].value_counts().head(20).index
sub_nodes = list(top_commenters) + [v for u, v in G.edges() if u in top_commenters]
subG = G.subgraph(sub_nodes)

plt.figure(figsize=(12,8))
pos = nx.spring_layout(subG, k=0.5, seed=42)
nx.draw(subG, pos, with_labels=True, node_size=500, node_color='skyblue', edge_color='gray', font_size=8)
plt.title("Commenter-Video Network (Top 20 Commenters)")
plt.show()


# Assuming you already have your graph 'G' and 'df' DataFrame
# where df has columns: ['author', 'video_title', 'video_id', 'sentiment']

# Create a subgraph if you want to focus on top commenters
top_commenters = df['author'].value_counts().head(20).index
sub_nodes = list(top_commenters) + [v for u, v in G.edges() if u in top_commenters]
subG = G.subgraph(sub_nodes)

# Generate layout
pos = nx.spring_layout(subG, k=0.5, seed=42)

# Color edges based on sentiment
edge_colors = []
for u, v in subG.edges():
    if 'sentiment' in subG[u][v]:
        sentiment = subG[u][v]['sentiment']
        if sentiment == 'positive':
            edge_colors.append('green')
        elif sentiment == 'negative':
            edge_colors.append('red')
        else:
            edge_colors.append('gray')
    else:
        edge_colors.append('gray')

# Draw nodes
nx.draw_networkx_nodes(subG, pos, node_color='skyblue', node_size=500)
# Draw edges
nx.draw_networkx_edges(subG, pos, edge_color=edge_colors, arrows=True)
# Draw labels
nx.draw_networkx_labels(subG, pos, font_size=8)

plt.title("YouTube Commenter-Video Network Colored by Sentiment")
plt.axis('off')
plt.show()

