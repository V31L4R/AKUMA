from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AdvancedPage(QWidget):
    def __init__(self):
        super().__init__()
        page_layout = QVBoxLayout()
        self.setLayout(page_layout)
        page_title = QLabel("Advanced")
        page_layout.addWidget(page_title)
        page_layout.addStretch()