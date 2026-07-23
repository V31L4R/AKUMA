import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AKUMA")
        self.resize(1000, 700)
        central_widget = QWidget()
        ##central_widget.setStyleSheet("background-color:white;") - test string to make sure that widget has been created 
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        sidebar = QWidget()
        content_area = QWidget()
        main_layout.addWidget(sidebar,1)
        main_layout.addWidget(content_area,4)
        sidebar.setStyleSheet("background-color: #202020;") 
        content_area.setStyleSheet("background-color: #303030;") 
        
        self.setCentralWidget(central_widget)



def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


