import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def recover(file_path, input_clusters, n_clusters, start_cluster):
    """
    Recovers and groups similar clusters based on semantic similarity using KMeans clustering.
    
    :param file_path: Path to the CSV file containing 'cluster_number' and 'content'.
    :param input_clusters: List of cluster numbers to be grouped.
    :param n_clusters: Number of clusters to form.
    :return: Dictionary of grouped clusters.
    """
    
    data = pd.read_csv(file_path, on_bad_lines='skip')  
    
    clusters = data['content'].tolist()  
    cluster_numbers = data['cluster_number'].tolist()  

   
    model = SentenceTransformer('all-MiniLM-L6-v2') 
    embeddings = model.encode(clusters)  

   
    def calculate_similarity_matrix(embeddings):
        return cosine_similarity(embeddings)

    filtered_clusters = []
    filtered_indices = []
    for cluster_num in input_clusters:
        if cluster_num in cluster_numbers:
            idx = cluster_numbers.index(cluster_num)
            filtered_clusters.append(clusters[idx])
            filtered_indices.append(idx)
    
    filtered_embeddings = [embeddings[idx] for idx in filtered_indices]
    
    similarity_matrix = calculate_similarity_matrix(filtered_embeddings)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, init='k-means++', n_init=100, max_iter=500)
    labels = kmeans.fit_predict(filtered_embeddings)
    
    file_groups = {i: [] for i in range(n_clusters)}  
    for i, label in enumerate(labels):
        file_groups[label].append(input_clusters[i])  
    
    grouped_files = {f"Group {i+1}": sorted(group) for i, group in file_groups.items()}
    return grouped_files



def print_clusters(grouped_clusters, start_cluster):
    
    print("\nFiles Grouped by Similarity and Semantic Context:")
    for file, clusters in grouped_clusters.items():
        clusters_str = ', '.join(map(str, clusters))
        # Highlight the start cluster in the printout
        if start_cluster in clusters:
            print(f"{file} -> Clusters {clusters_str} ")
        # else:
        #     print(f"{file} -> Clusters {clusters_str}")




file_path = 'data.csv'
input_clusters = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 18]
grouped_clusters = recover(file_path, input_clusters, n_clusters=5, start_cluster=4)


print_clusters(grouped_clusters,start_cluster=4)
