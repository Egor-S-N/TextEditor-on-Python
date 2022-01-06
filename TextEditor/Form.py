
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QFileDialog, QLabel, QMenu, QShortcut, QTextEdit, QMainWindow, QMessageBox
import re


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initForm()

    def initForm(self):
        self.setGeometry(100, 100, 700, 500)

        self.textBar = QLabel("Testing")
        self.Bar = self.statusBar()
        self.Bar.addPermanentWidget(self.textBar)

        self.Menu = self.menuBar()

        self.FileMenu = QMenu("&File", self)
        self.FileMenu.addAction('&Open file', self.OpenFile)
        self.FileMenu.addAction('&Save file', self.SaveFile)
        self.FileMenu.addAction('&Save file as', self.SavaFileAs)
        self.FileMenu.addAction('&New file', self.NewFile)

        self.Menu.addMenu(self.FileMenu)

        self.TextEditor = QTextEdit(self)
        self.TextEditor.setGeometry(3, 21, 695, 200)
        self.TextEditor.textChanged.connect(self.ContentCount)

        self.ShotCatOpen = QShortcut(QKeySequence("Ctrl+O"), self)
        self.ShotCatOpen.activated.connect(self.OpenFile)

        self.ShotCatSave = QShortcut(QKeySequence("Ctrl+S"), self)
        self.ShotCatSave.activated.connect(self.SaveFile)

        self.ShotCatSaveAs = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        self.ShotCatSaveAs.activated.connect(self.SavaFileAs)

        self.ShotCatNewFile = QShortcut(QKeySequence("Ctrl+Shift+N"), self)
        self.ShotCatNewFile.activated.connect(self.NewFile)

        self.File_path = ''

        self.show()

    def ContentCount(self):

        Content = self.TextEditor.toPlainText()
        # Подсчет кол-ва слов
        SplitContent = re.split(' |,  |: |; |\n', Content)

        SymblosCount = 0
        for symbol in Content:
            SymblosCount += 1  # Подсчет кол-ва символов

        LinesCount = Content.count('\n')  # Посчет кол-ва строк
        if not Content.endswith('\n'):
            LinesCount += 1

        self.Bar.showMessage('Кол-во слов: %s     Кол-во строк: %d     Кол-во символов: %s' %
                             (str(len(SplitContent)), LinesCount, int(SymblosCount)))

    def OpenFile(self):
        self.textBar.setText("Открытие файла")
        file, _ = QFileDialog.getOpenFileName(
            None, 'Open File', './', "TextFile (*.txt *.docx)")

        self.textBar.setText("Файл успешно открыт")
        self.File_path = file
        with open(file, "r") as ReadFile:
            Content = ReadFile.read()
        self.TextEditor.setText(Content)

    def SavaFileAs(self):
        file, _ = QFileDialog.getSaveFileName(
            None, 'Save file', './', "TextFile (*.txt *.docx)")
        with open(file,  "w") as SaveAs:
            SaveAs.write(self.TextEditor.toPlainText())
        self.File_path = file
        self.textBar.setText("Новый файл сохранен")

    def SaveFile(self):

        if(self.File_path != ""):
            with open(self.File_path, "w") as WriteFile:
                WriteFile.write(self.TextEditor.toPlainText())
            self.textBar.setText("Документ сохранен")
        else:
            self.SavaFileAs()

    def NewFile(self):  # Отредактировать метод а то хули он на все работает
        if self.TextEditor.toPlainText() != "":
            msg = QMessageBox.question(
                self,
                'Label',
                'Файл не был сохранен\nХотите сохранить?',
                QMessageBox.Ok | QMessageBox.Cancel,

            )

            if msg == QMessageBox.Ok:
                if self.File_path != '':
                    self.SaveFile()
                else:
                    self.SavaFileAs()
                self.File_path = ''
                self.TextEditor.setText("")
            elif msg == QMessageBox.Cancel:
                self.File_path = ''
                self.TextEditor.setText("")
        self.textBar.setText("Новый файл создан")

    def closeEvent(self, event):
        result = QMessageBox.question(self, "Подтверждение закрытия окна",
                                      "Вы действительно хотите закрыть окно?",
                                      QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)
        if result == QMessageBox.Yes:
            event.accept()
            self.closeEvent(self, event)
        else:
            event.ignore()
