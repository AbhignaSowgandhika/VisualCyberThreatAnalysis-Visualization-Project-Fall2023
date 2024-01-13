import matplotlib.pyplot as plt
import pandas as pd

def load_and_plot_graphs(file_path, graph_type):
    data = pd.read_csv(file_path, header=None)

    attack_types = data.iloc[:, -1]

    if graph_type=="bar":
        fig = plt.figure(figsize=(10, 6))
        attack_types.value_counts().plot(kind='bar', color='skyblue')
        plt.title('Number of Attacks by Type')
        plt.xlabel('Attack Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
    elif graph_type == "pie":
        fig = plt.figure(figsize=(8, 8))
        plt.pie(attack_types.value_counts(), startangle=90, colors=plt.cm.Paired.colors)
        plt.title('Distribution of Attacks by Type')
    return fig

if __name__ == "__main__":
    file_path = input("Enter file name: ").strip()
    load_and_plot_graphs(file_path, "bar")
    plt.show()
