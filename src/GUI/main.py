import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AKUMA")
        self.resize(1000, 700)
        central_widget = QWidget()
        ##central_widget.setStyleSheet("background-color:white;") - test string to make sure that widget has been created 
        self.setCentralWidget(central_widget)



def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()


