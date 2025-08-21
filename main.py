import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from itertools import combinations
from collections import defaultdict

# --- Configuration ---
JSON_FOLDER = "JSONS"
OUTPUT_FOLDER = "graphs_professional" # Use a new folder to avoid overwriting

def setup_professional_style():
    """
    Sets matplotlib parameters for a professional, paper-like style.
    """
    plt.style.use('default') # Start from a clean slate
    
    # Font settings for a more academic look (STIX is a Times-like font)
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': 'STIXGeneral',
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        
        # Colors
        'axes.labelcolor': '#333333',
        'text.color': '#333333',
        'xtick.color': '#333333',
        'ytick.color': '#333333',
        'axes.edgecolor': '#333333',
        
        # Remove unnecessary chart borders ("spines")
        'axes.spines.top': False,
        'axes.spines.right': False,
        
        # Figure background
        'figure.facecolor': 'white',
        'axes.facecolor': 'white'
    })

def load_all_data(folder_path):
    """
    Loads and combines all JSON files from a specified folder.
    """
    all_exercises = []
    if not os.path.exists(folder_path):
        print(f"Error: The directory '{folder_path}' was not found.")
        return None

    print(f"Loading data from '{folder_path}'...")
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_exercises.extend(data)
    
    print(f"Successfully loaded {len(all_exercises)} exercises in total.")
    return all_exercises

def save_plot(output_path):
    """
    Saves the current plot with tight bounding box and high resolution.
    """
    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches='tight', # Crop to the content
        pad_inches=0.05     # Add a tiny bit of padding
    )
    plt.close()
    print(f"Graph saved to '{output_path}'")

def create_topic_distribution_chart(df, output_path):
    """
    Creates a minimalist horizontal bar chart of exercise counts per topic.
    """
    print("Generating 'Exercises per Topic' chart...")
    topics_df = df.explode('topics')
    
    plt.figure(figsize=(8, 6))
    # Use a single, professional color
    sns.countplot(y='topics', data=topics_df, order=topics_df['topics'].value_counts().index, color='#4c566a')
    
    plt.xlabel('') # Remove x-axis label
    plt.ylabel('') # Remove y-axis label
    
    # Add subtle vertical grid lines for readability
    plt.grid(axis='x', linestyle='--', alpha=0.6, linewidth=0.5)
    
    save_plot(output_path)

def create_source_distribution_chart(df, output_path):
    """
    Creates a minimalist horizontal bar chart of exercise counts per source PDF.
    """
    print("\nGenerating 'Exercises per Source PDF' chart...")
    plt.figure(figsize=(8, 5))
    sns.countplot(y='source_pdf', data=df, order=df['source_pdf'].value_counts().index, color='#5e81ac')
    
    plt.xlabel('')
    plt.ylabel('')
    plt.grid(axis='x', linestyle='--', alpha=0.6, linewidth=0.5)
    
    save_plot(output_path)

def create_topic_network_graph(df, output_path):
    """
    Creates a minimalist network graph of co-occurring topics.
    """
    print("\nGenerating 'Topic Co-occurrence Network' graph...")
    
    co_occurrence = defaultdict(int)
    for topics in df['topics']:
        if len(topics) > 1:
            for pair in combinations(sorted(topics), 2):
                co_occurrence[pair] += 1
            
    if not co_occurrence:
        print("No topic co-occurrences found. Skipping network graph.")
        return

    G = nx.Graph()
    for (topic1, topic2), weight in co_occurrence.items():
        G.add_edge(topic1, topic2, weight=weight)
        
    topic_counts = df.explode('topics')['topics'].value_counts()
    node_sizes = [topic_counts.get(node, 1) * 70 for node in G.nodes()]
    edge_widths = [d['weight'] * 0.4 for u, v, d in G.edges(data=True)]

    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.9, iterations=50, seed=42)
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='#d8dee9', edgecolors='#4c566a')
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color='#888888', alpha=0.7)
    nx.draw_networkx_labels(G, pos, font_size=9, font_family='serif', font_color='#2e3440')
    
    # Remove all borders and axes from the plot
    plt.axis('off')
    
    save_plot(output_path)


def main():
    """
    Main function to run the script.
    """
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Set the visual style for all plots
    setup_professional_style()
    print("Using professional, paper-like style for graphs.")

    exercise_data = load_all_data(JSON_FOLDER)
    if not exercise_data:
        return
        
    df = pd.DataFrame(exercise_data)

    create_topic_distribution_chart(df, os.path.join(OUTPUT_FOLDER, "topics_distribution.png"))
    create_source_distribution_chart(df, os.path.join(OUTPUT_FOLDER, "source_distribution.png"))
    create_topic_network_graph(df, os.path.join(OUTPUT_FOLDER, "topic_network.png"))
    
    print("\nAll graphs have been generated successfully!")

if __name__ == "__main__":
    main()