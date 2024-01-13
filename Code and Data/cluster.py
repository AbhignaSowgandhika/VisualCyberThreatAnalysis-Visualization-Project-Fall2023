import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans

def load_data(file_name):
    df = pd.read_csv(file_name, header=None)

    columns = [
        'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
        'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins',
        'logged_in', 'num_compromised', 'root_shell', 'su_attempted', 'num_root',
        'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
        'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate',
        'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate', 'same_srv_rate',
        'diff_srv_rate', 'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
        'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
        'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
        'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'attack_type'
    ]

    df.columns = columns

    symbolic_columns = ['protocol_type', 'service', 'flag', 'attack_type']

    le = LabelEncoder()
    for col in symbolic_columns:
        df[col] = le.fit_transform(df[col])

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df.drop('attack_type', axis=1))

    return df_scaled, df['attack_type']

def perform_kmeans(df, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans_result = kmeans.fit_predict(df)

    df_kmeans = pd.DataFrame(df, columns=[f'Dimension {i+1}' for i in range(df.shape[1])])
    df_kmeans['Cluster'] = kmeans_result

    fig, ax = plt.subplots(figsize=(10, 8))
    scatter = ax.scatter(df_kmeans['Dimension 1'], df_kmeans['Dimension 2'], c=df_kmeans['Cluster'], cmap='viridis', alpha=0.5)

    centers = kmeans.cluster_centers_
    radii = [np.linalg.norm(point - center) for point, center in zip(df, centers)]
    circles = [plt.Circle(center, radius, alpha=0.5, edgecolor='black') for center, radius in zip(centers, radii)]
    for circle in circles:
        ax.add_patch(circle)

    ax.set_title('K-Means Clustering with Cluster Circles')
    ax.legend(*scatter.legend_elements(), title='Clusters')
    
    return fig

if __name__ == "__main__":
    file_path = input("Enter filename: ").strip()
    data, attack_types = load_data(file_path)
    num_clusters = len(attack_types.unique())
    kmeans_figure = perform_kmeans(data, num_clusters)
    plt.show()
