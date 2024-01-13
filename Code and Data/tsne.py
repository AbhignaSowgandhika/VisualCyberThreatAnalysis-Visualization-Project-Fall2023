import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

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
        'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'class'
    ]

    df.columns = columns

    le = LabelEncoder()
    df['protocol_type'] = le.fit_transform(df['protocol_type'])
    df['service'] = le.fit_transform(df['service'])
    df['flag'] = le.fit_transform(df['flag'])
    df['logged_in'] = le.fit_transform(df['logged_in'])
    df['is_host_login'] = le.fit_transform(df['is_host_login'])
    df['is_guest_login'] = le.fit_transform(df['is_guest_login'])
    df['class'] = le.fit_transform(df['class'])

    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df.drop('class', axis=1))

    return df_scaled, df['class']

def perform_tsne(df_scaled, class_labels):
    tsne = TSNE(n_components=2, random_state=42)
    tsne_result = tsne.fit_transform(df_scaled)

    tsne_df = pd.DataFrame(tsne_result, columns=['Dimension 1', 'Dimension 2'])
    tsne_df['class'] = class_labels

    fig = plt.figure(figsize=(10, 8))
    scatter = plt.scatter(tsne_df['Dimension 1'], tsne_df['Dimension 2'], c=tsne_df['class'], cmap='viridis')
    plt.title('t-SNE Visualization')
    plt.legend(*scatter.legend_elements(), title='Classes')
    return fig

if __name__ == "__main__":
    file_path = input("Enter filename: ").strip()
    data, class_labels = load_data(file_path)
    pca_figure = perform_tsne(data, class_labels)
    plt.show()