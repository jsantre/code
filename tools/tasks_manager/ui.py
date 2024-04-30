import sys, os

from PySide2 import QtWidgets, QtCore, QtGui

import manage_tasks


ICONS_FOLDER = os.path.join(os.path.dirname(__file__), "icons")
COLOR_STATUS = {False: (116, 227, 225), True: (218, 226, 225)}
COLOR_TEXT = {False: (1, 1, 1), True: (118, 126, 125)}


class TaskItem(QtWidgets.QListWidgetItem):
    def __init__(self, task_name, done):
        """init the class
        :param task_name: task name to create
        :type task_name: str
        :param done: task status
        :type done: bool
        """
        super(TaskItem, self).__init__(task_name)

        self.task_name = task_name
        self.done = done

        self.setSizeHint(QtCore.QSize(self.sizeHint().width(), 50))
        self.setTextAlignment(QtCore.Qt.AlignCenter)
        self.set_color()

    def set_color(self):
        """set color matching with task status"""
        self.setBackgroundColor(QtGui.QColor(*COLOR_STATUS[self.done]))
        self.setForeground(QtGui.QColor(*COLOR_TEXT[self.done]))

    def toggle_status(self):
        self.done = not self.done
        manage_tasks.set_task_status(name=self.task_name, status=self.done)
        self.set_color()


class TaskUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(TaskUI, self).__init__(parent)
        self.setWindowTitle("To Do List")
        self.setup_ui()
        self.update_tasks_display()

    def setup_ui(self):
        self.create_widgets()
        self.create_layouts()
        self.modifiy_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self):
        """Create needed widgets"""
        self.list_tasks = QtWidgets.QListWidget()
        self.btn_add = QtWidgets.QPushButton()
        self.btn_clean = QtWidgets.QPushButton()
        self.btn_quit = QtWidgets.QPushButton()

        self.tray = QtWidgets.QSystemTrayIcon()

    def create_layouts(self):
        """Create needed layouts"""
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.btns_layout = QtWidgets.QHBoxLayout()

    def modifiy_widgets(self):
        """modifiy created widgets"""
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # disable selection view and scrollbar
        self.list_tasks.setSelectionMode(QtWidgets.QListWidget.NoSelection)
        self.list_tasks.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_tasks.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # add icons to buttons
        self.btn_add.setIcon(QtGui.QIcon(os.path.join(ICONS_FOLDER, "add.svg")))
        self.btn_clean.setIcon(QtGui.QIcon(os.path.join(ICONS_FOLDER, "clean.svg")))
        self.btn_quit.setIcon(QtGui.QIcon(os.path.join(ICONS_FOLDER, "close.svg")))

        # set icon size
        self.btn_add.setFixedSize(20, 20)
        self.btn_clean.setFixedSize(20, 20)
        self.btn_quit.setFixedSize(20, 20)

        # disable borders
        self.setStyleSheet("border:none;")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # set tray icon
        icon_path = os.path.join(ICONS_FOLDER, "icon.png")
        self.tray.setIcon(QtGui.QIcon(icon_path))
        self.tray.setVisible(True)

    def add_widgets_to_layouts(self):
        """Add created widgets to layouts"""
        self.main_layout.addWidget(self.list_tasks)
        self.main_layout.addLayout(self.btns_layout)

        self.btns_layout.addWidget(self.btn_add)
        # add space after add btn
        self.btns_layout.addStretch()
        self.btns_layout.addWidget(self.btn_clean)
        self.btns_layout.addWidget(self.btn_quit)

    def setup_connections(self):
        """Connect widgets to actions"""
        self.btn_add.clicked.connect(self.add_task)
        self.btn_clean.clicked.connect(self.clean_task)
        self.btn_quit.clicked.connect(self.close)
        self.list_tasks.itemClicked.connect(lambda item: item.toggle_status())
        self.tray.activated.connect(self.toggle_visibility)

    def add_task(self):
        """Open dialog to add new task"""
        task_name, validate = QtWidgets.QInputDialog.getText(
            self, "Add Task", "Task name:"
        )
        if validate and task_name:
            manage_tasks.add_task(task_name)
            task_item = TaskItem(task_name, False)
            self.list_tasks.addItem(task_item)

    def clean_task(self):
        """clean task done"""
        for item_index in range(self.list_tasks.count()):
            item = self.list_tasks.item(item_index)
            if item.done:
                manage_tasks.remove_task(item.task_name)
        self.update_tasks_display()

    def update_tasks_display(self):
        """refresh display with new data"""
        self.list_tasks.clear()
        tasks = manage_tasks.get_tasks()
        for task_name, done in tasks.items():
            task_item = TaskItem(task_name, done)
            self.list_tasks.addItem(task_item)

        # force refresh display
        self.list_tasks.repaint()

    def toggle_visibility(self):
        """toggle window visibility"""
        if self.isHidden():
            self.showNormal()
        else:
            self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TaskUI()
    window.show()
    sys.exit(app.exec_())
