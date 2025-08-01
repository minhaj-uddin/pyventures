import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QFileDialog, QLabel,
    QColorDialog, QStatusBar, QMenu, QMenuBar, QSpinBox
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QIcon, QColor, QImage
from PyQt5.QtCore import Qt, QPoint


class PaintCanvas(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.image = QImage(600, 600, QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.setPixmap(QPixmap.fromImage(self.image))

        self.drawing = False
        self.pen_color = Qt.black
        self.pen_width = 3
        self.tool = "Brush"
        self.last_point = QPoint()
        self.undo_stack = []
        self.redo_stack = []
        self.clipboard = QApplication.clipboard()
        self.parent = parent

    def resizeEvent(self, event):
        new_image = QImage(self.size(), QImage.Format_RGB32)
        new_image.fill(Qt.white)
        painter = QPainter(new_image)
        painter.drawImage(QPoint(), self.image)
        self.image = new_image
        self.setPixmap(QPixmap.fromImage(self.image))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.save_undo()
            self.drawing = True
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        self.parent.statusBar().showMessage(
            f"Coordinates: ({event.x()}, {event.y()})")
        if self.drawing and (event.buttons() & Qt.LeftButton):
            painter = QPainter(self.image)
            pen = QPen(Qt.white if self.tool == "Eraser" else self.pen_color,
                       self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.setPixmap(QPixmap.fromImage(self.image))

    def mouseReleaseEvent(self, event):
        self.drawing = False

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        undo_action = menu.addAction(QIcon("icons/undo.png"), "Undo")
        redo_action = menu.addAction(QIcon("icons/redo.png"), "Redo")
        menu.addSeparator()
        copy_action = menu.addAction(QIcon("icons/copy.png"), "Copy")
        paste_action = menu.addAction(QIcon("icons/paste.png"), "Paste")
        menu.addSeparator()
        clear_action = menu.addAction(QIcon("icons/clear.png"), "Clear")
        action = menu.exec_(self.mapToGlobal(event.pos()))

        if action == undo_action:
            self.undo()
        elif action == redo_action:
            self.redo()
        elif action == copy_action:
            self.copy()
        elif action == paste_action:
            self.paste()
        elif action == clear_action:
            self.clear_canvas()

    def set_tool(self, tool):
        self.tool = tool

    def set_pen_color(self, color):
        self.pen_color = color

    def set_pen_width(self, width):
        self.pen_width = width

    def clear_canvas(self):
        self.save_undo()
        self.image.fill(Qt.white)
        self.setPixmap(QPixmap.fromImage(self.image))

    def save_undo(self):
        self.undo_stack.append(self.image.copy())
        self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.image.copy())
            self.image = self.undo_stack.pop()
            self.setPixmap(QPixmap.fromImage(self.image))

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.setPixmap(QPixmap.fromImage(self.image))

    def copy(self):
        self.clipboard.setImage(self.image)

    def paste(self):
        pasted_image = self.clipboard.image()
        if not pasted_image.isNull():
            self.save_undo()
            self.image = pasted_image.scaled(self.size(), Qt.KeepAspectRatio)
            self.setPixmap(QPixmap.fromImage(self.image))

    def save_image(self, path):
        self.image.save(path)

    def open_image(self, path):
        loaded = QImage(path)
        if not loaded.isNull():
            self.save_undo()
            self.image = loaded.scaled(self.size(), Qt.KeepAspectRatio)
            self.setPixmap(QPixmap.fromImage(self.image))


class PaintApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Paint")
        self.setGeometry(100, 100, 1000, 700)

        self.canvas = PaintCanvas(self)
        self.setCentralWidget(self.canvas)

        self._create_toolbar()
        self._create_statusbar()
        self._create_menubar()

    def _create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        def act(icon, name, handler):
            action = QAction(QIcon(f"icons/{icon}.png"), name, self)
            action.triggered.connect(handler)
            toolbar.addAction(action)

        act("open", "Open", self.open_file)
        act("save", "Save", self.save_file)
        act("brush", "Brush", lambda: self.canvas.set_tool("Brush"))
        act("eraser", "Eraser", lambda: self.canvas.set_tool("Eraser"))
        act("color", "Color", self.choose_color)
        act("undo", "Undo", self.canvas.undo)
        act("redo", "Redo", self.canvas.redo)

        toolbar.addSeparator()
        toolbar.addWidget(QLabel(" Brush Size: "))

        size_selector = QSpinBox()
        size_selector.setRange(1, 50)
        size_selector.setValue(3)
        size_selector.valueChanged.connect(self.canvas.set_pen_width)
        toolbar.addWidget(size_selector)

    def _create_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Ready")

    def _create_menubar(self):
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu("File")
        file_menu.addAction(QIcon("icons/open.png"), "Open", self.open_file)
        file_menu.addAction(QIcon("icons/save.png"), "Save", self.save_file)

        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction(QIcon("icons/undo.png"), "Undo", self.canvas.undo)
        edit_menu.addAction(QIcon("icons/redo.png"), "Redo", self.canvas.redo)

        self.setMenuBar(menubar)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_pen_color(color)
            self.statusBar().showMessage(f"Color selected: {color.name()}")

    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
        if path:
            self.canvas.save_image(path)
            self.statusBar().showMessage(f"Saved to {path}")

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.bmp)")
        if path:
            self.canvas.open_image(path)
            self.statusBar().showMessage(f"Loaded {path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintApp()
    window.show()
    sys.exit(app.exec_())
