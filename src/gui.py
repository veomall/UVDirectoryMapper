import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QComboBox, QLineEdit, QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox,
                             QStackedWidget, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
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

        # Load styles from external file
        with open('src/styles.qss', 'r') as f:
            self.setStyleSheet(f.read())

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create a splitter
        splitter = QSplitter(Qt.Vertical)

        # Top widget (for input controls)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)

        # Viewer selection
        viewer_layout = QHBoxLayout()
        self.viewer_combo = QComboBox()
        self.viewer_combo.addItems(["Local Directory", "Archive", "GitHub Repository"])
        self.viewer_combo.currentIndexChanged.connect(self.on_viewer_changed)
        viewer_layout.addWidget(QLabel("Select Viewer:"))
        viewer_layout.addWidget(self.viewer_combo)
        top_layout.addLayout(viewer_layout)

        # Path input
        self.path_stack = QStackedWidget()

        # Local and Archive
        self.file_select_widget = QWidget()
        file_select_layout = QHBoxLayout(self.file_select_widget)
        self.path_input = QLineEdit()
        self.path_input.setFixedHeight(25)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        file_select_layout.addWidget(self.path_input)
        file_select_layout.addWidget(self.browse_button)

        # GitHub
        self.github_input = QLineEdit()
        self.github_input.setPlaceholderText("Enter GitHub repository URL")
        self.github_input.setFixedHeight(25)

        self.path_stack.addWidget(self.file_select_widget)
        self.path_stack.addWidget(self.github_input)

        top_layout.addWidget(self.path_stack)

        # Exclusions
        exclusions_layout = QHBoxLayout()
        self.exclusions_input = QLineEdit()
        self.exclusions_input.setPlaceholderText("Enter comma-separated folder names to exclude")
        self.exclusions_input.setFixedHeight(25)
        exclusions_layout.addWidget(QLabel("Exclusions:"))
        exclusions_layout.addWidget(self.exclusions_input)
        top_layout.addLayout(exclusions_layout)

        # Open button
        self.open_button = QPushButton("Open")
        self.open_button.clicked.connect(self.open_tree)
        top_layout.addWidget(self.open_button)

        # Add top widget to splitter
        splitter.addWidget(top_widget)

        # Bottom widget (for tree view and save button)
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)

        # Tree view
        self.tree_view = QTextEdit()
        self.tree_view.setReadOnly(True)
        bottom_layout.addWidget(self.tree_view)

        # Save image button
        self.save_image_button = QPushButton("Save Tree Image")
        self.save_image_button.clicked.connect(self.save_tree_image)
        bottom_layout.addWidget(self.save_image_button)

        # Add bottom widget to splitter
        splitter.addWidget(bottom_widget)

        # Set initial sizes
        splitter.setSizes([200, 400])  # Adjust these values as needed

        # Add splitter to main layout
        main_layout.addWidget(splitter)

        self.config = Config()

    def on_viewer_changed(self, index):
        if index == 2:  # GitHub
            self.path_stack.setCurrentIndex(1)
        else:  # Local or Archive
            self.path_stack.setCurrentIndex(0)

    def browse_file(self):
        if self.viewer_combo.currentIndex() == 0:  # Local Directory
            path = QFileDialog.getExistingDirectory(self, "Select Directory")
        else:  # Archive
            path, _ = QFileDialog.getOpenFileName(self, "Select Archive", "", "Archives (*.zip *.tar *.rar)")

        if path:
            self.path_input.setText(path)
    
    def open_tree(self):
        viewer_type = self.viewer_combo.currentIndex()

        if viewer_type == 2:  # GitHub
            path = self.github_input.text()
        else:
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
