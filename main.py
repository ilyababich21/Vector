import sys

from PyQt6.QtWidgets import QApplication

from VectorWin import VectorWin


def main():
    app = QApplication(sys.argv)
    window = VectorWin()
    window.show()

    app.exec()

if __name__ == "__main__":
    main()