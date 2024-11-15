import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QComboBox, QLineEdit, QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from src.tree_viewers.local_viewer import LocalViewer
from src.tree_viewers.archive_viewer import ArchiveViewer
from src.tree_viewers.github_viewer import GitHubViewer
from src.config import Config
from src.utils.image_creator import create_tree_image


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UVDirectoryMapper")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Viewer selection
        viewer_layout = QHBoxLayout()
        self.viewer_combo = QComboBox()
        self.viewer_combo.addItems(["Local Directory", "Archive", "GitHub Repository"])
        viewer_layout.addWidget(QLabel("Select Viewer:"))
        viewer_layout.addWidget(self.viewer_combo)
        layout.addLayout(viewer_layout)

        # Path input
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        path_layout.addWidget(QLabel("Path:"))
        path_layout.addWidget(self.path_input)
        layout.addLayout(path_layout)

        # Exclusions
        exclusions_layout = QHBoxLayout()
        self.exclusions_input = QLineEdit()
        exclusions_layout.addWidget(QLabel("Exclusions:"))
        exclusions_layout.addWidget(self.exclusions_input)
        layout.addLayout(exclusions_layout)

        # Open button
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_tree)
        layout.addWidget(self.open_button)

        # Tree view
        self.tree_view = QTextEdit()
        self.tree_view.setReadOnly(True)
        layout.addWidget(self.tree_view)

        # Save image button
        self.save_image_button = QPushButton("Save Tree Image")
        self.save_image_button.clicked.connect(self.save_tree_image)
        layout.addWidget(self.save_image_button)

        self.config = Config()

    def open_tree(self):
        viewer_type = self.viewer_combo.currentIndex()
        path = self.path_input.text()
        exclusions = self.exclusions_input.text().split(',')
        
        for exclusion in exclusions:
            self.config.add_excluded_folder(exclusion.strip())

        if viewer_type == 0 and os.path.isdir(path):
            viewer = LocalViewer()
        elif viewer_type == 1 and ArchiveViewer.is_archive(path):
            viewer = ArchiveViewer()
        elif viewer_type == 2 and GitHubViewer.is_github_url(path):
            viewer = GitHubViewer()
        else:
            QMessageBox.warning(self, "Error", "Invalid viewer type or path")
            return

        try:
            tree_str = viewer.view(path, self.config)
            self.tree_view.setText(tree_str)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def save_tree_image(self):
        tree_str = self.tree_view.toPlainText()
        if not tree_str:
            QMessageBox.warning(self, "Error", "No tree to save")
            return

        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Tree Image", downloads_path, "PNG Files (*.png)")
        
        if file_path:
            try:
                create_tree_image(tree_str, file_path.rsplit('.', 1)[0])
                QMessageBox.information(self, "Success", f"Image saved to {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save image: {str(e)}")

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()
