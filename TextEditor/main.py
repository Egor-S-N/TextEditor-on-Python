import sys, Form

from PyQt5 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Form.MainForm()
    sys.exit(app.exec_())
     