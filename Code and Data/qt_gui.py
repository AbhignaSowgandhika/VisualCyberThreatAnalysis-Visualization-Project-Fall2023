import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pca import load_data as load_pca_data, perform_pca
from tsne import load_data as load_tsne_data, perform_tsne
from cluster import load_data as load_clusters_data, perform_kmeans
from graphs import load_and_plot_graphs

class VisualizationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.selected_method = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        
        self.visualization_widget = QWidget()
        self.visualization_layout = QVBoxLayout(self.visualization_widget)
        
        self.options_widget = QWidget()
        self.options_layout = QVBoxLayout(self.options_widget)
        
        self.method_dropdown = QComboBox()
        self.method_dropdown.addItems(["Select Method", "PCA", "t-SNE", "Clusters", "Bar Graph", "Pie Chart"])
        self.method_dropdown.currentIndexChanged.connect(self.update_method)
        
        self.open_dataset_button = QPushButton("Open Dataset")
        self.open_dataset_button.clicked.connect(self.open_dataset)

        self.dataset_label = QLabel("No dataset selected")
        self.dataset_label.setMaximumHeight(10)
        
        self.options_layout.addWidget(self.dataset_label)
        self.options_layout.addWidget(self.open_dataset_button)
        self.options_layout.addWidget(self.method_dropdown)
        
        layout.addWidget(self.visualization_widget, 3)
        layout.addWidget(self.options_widget, 1)

        self.setLayout(layout)
        self.setWindowTitle('COSC 6344 Visualization - Project , LOKESH, GIDEON, ABHIGNA')

    def open_dataset(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Dataset", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.data = file_name
            self.show_data()

    def update_method(self, index):
        self.selected_method = self.method_dropdown.currentText()
        if self.data is not None and self.selected_method != "Select Method":
            self.visualize_data()

    def show_data(self):
        file_name_without_path = os.path.basename(self.data)
        self.dataset_label.setText(file_name_without_path)

    def visualize_data(self):
        if self.visualization_layout.count() > 0:
            previous_widget = self.visualization_layout.itemAt(0).widget()
            self.visualization_layout.removeWidget(previous_widget)
            previous_widget.setParent(None)
        if self.selected_method == "PCA":
            df_scaled = load_pca_data(self.data)
            self.plot_and_display(df_scaled, class_labels=["empty"], plot_function=perform_pca)
        elif self.selected_method == "t-SNE":
            
            df_scaled, class_labels = load_tsne_data(self.data)
            self.plot_and_display(df_scaled, class_labels=class_labels, plot_function=perform_tsne)
        elif self.selected_method == "Clusters":
            df_scaled, class_labels = load_clusters_data(self.data)
            self.plot_and_display(df_scaled, class_labels=class_labels, plot_function=perform_kmeans)
        elif self.selected_method == "Bar Graph":
            self.plot_and_display(self.data, class_labels=["bar"], plot_function=load_and_plot_graphs)
        elif self.selected_method == "Pie Chart":
            self.plot_and_display(self.data, class_labels=["pie"], plot_function=load_and_plot_graphs)

    def plot_and_display(self, df_scaled, class_labels=None, plot_function=None):
        if class_labels is None or plot_function is None:
            return
        if plot_function == perform_tsne:
            fig = plot_function(df_scaled, class_labels)
        elif plot_function == perform_pca:
            fig = plot_function(df_scaled)
        elif plot_function == perform_kmeans:
            fig = plot_function(df_scaled, len(class_labels.unique()))
        else:
            fig = plot_function(df_scaled, class_labels[0])
        canvas = FigureCanvas(fig)
        self.visualization_layout.addWidget(canvas)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VisualizationApp()
    window.setGeometry(100, 100, 800, 400)
    window.show()
    sys.exit(app.exec_())
