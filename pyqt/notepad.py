import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QAction, QFileDialog,
    QToolBar, QStatusBar, QColorDialog, QFontDialog, QMessageBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Notepad")
        self.setGeometry(100, 100, 800, 600)

        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        self._create_actions()
        self._create_menu()
        self._create_toolbar()
        self._create_statusbar()

    def _create_actions(self):
        self.new_action = QAction(QIcon("icons/new.png"), "New", self)
        self.new_action.setShortcut("Ctrl+N")
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction(QIcon("icons/open.png"), "Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction(QIcon("icons/save.png"), "Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)

        self.cut_action = QAction(QIcon("icons/cut.png"), "Cut", self)
        self.cut_action.setShortcut("Ctrl+X")
        self.cut_action.triggered.connect(self.editor.cut)

        self.copy_action = QAction(QIcon("icons/copy.png"), "Copy", self)
        self.copy_action.setShortcut("Ctrl+C")
        self.copy_action.triggered.connect(self.editor.copy)

        self.paste_action = QAction(QIcon("icons/paste.png"), "Paste", self)
        self.paste_action.setShortcut("Ctrl+V")
        self.paste_action.triggered.connect(self.editor.paste)

        self.undo_action = QAction(QIcon("icons/undo.png"), "Undo", self)
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.triggered.connect(self.editor.undo)

        self.redo_action = QAction(QIcon("icons/redo.png"), "Redo", self)
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.triggered.connect(self.editor.redo)

        self.font_action = QAction("Font", self)
        self.font_action.triggered.connect(self.choose_font)

        self.color_action = QAction("Color", self)
        self.color_action.triggered.connect(self.choose_color)

        self.about_action = QAction("About", self)
        self.about_action.triggered.connect(self.about)

    def _create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        edit_menu = menu.addMenu("Edit")
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)

        format_menu = menu.addMenu("Format")
        format_menu.addAction(self.font_action)
        format_menu.addAction(self.color_action)

        help_menu = menu.addMenu("Help")
        help_menu.addAction(self.about_action)

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.cut_action)
        toolbar.addAction(self.copy_action)
        toolbar.addAction(self.paste_action)
        toolbar.addSeparator()
        toolbar.addAction(self.undo_action)
        toolbar.addAction(self.redo_action)

    def _create_statusbar(self):
        statusbar = QStatusBar()
        self.setStatusBar(statusbar)
        self.editor.cursorPositionChanged.connect(self.update_statusbar)
        self.update_statusbar()

    def update_statusbar(self):
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.statusBar().showMessage(f"Line: {line}, Column: {col}")

    def new_file(self):
        self.editor.clear()

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt);;All Files (*)")
        if path:
            with open(path, 'r') as f:
                self.editor.setText(f.read())

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt);;All Files (*)")
        if path:
            with open(path, 'w') as f:
                f.write(self.editor.toPlainText())

    def choose_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.editor.setFont(font)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.editor.setTextColor(color)

    def about(self):
        QMessageBox.about(self, "About Notepad",
                          "PyQt5 Notepad Application Example")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Notepad()
    window.show()
    sys.exit(app.exec_())
