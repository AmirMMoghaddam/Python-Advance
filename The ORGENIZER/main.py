import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QWidget, QStackedWidget, QLineEdit, QSpinBox,
    QMessageBox, QListWidget, QListWidgetItem
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QSize
import database

class TheOrganizationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_task = None

    def init_ui(self):
        self.setWindowTitle('The Organization')
        self.setGeometry(100, 100, 800, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
            QPushButton {
                background-color: #4d4d4d;
                color: white;
                border: 1px solid #666666;
                border-radius: 5px;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #007acc;
            }
            QLabel {
                color: white;
            }
            QLineEdit, QSpinBox {
                background-color: #3c3c3c;
                color: white;
                border: none;
                border-bottom: 1px solid #666666;
                padding: 5px;
            }
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.header_label = QLabel("The Organization", self)
        self.header_label.setFont(QFont('Courier', 24, QFont.Bold))
        self.header_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.header_label)

        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        self.add_task_button = QPushButton('Add Task', self)
        self.add_task_button.setFont(QFont('Courier', 14))
        self.add_task_button.setIcon(QIcon("icons/add_task.png"))
        self.add_task_button.setIconSize(QSize(24, 24))
        self.add_task_button.clicked.connect(self.open_add_task_window)
        self.button_layout.addWidget(self.add_task_button)

        self.get_task_button = QPushButton('Get Task', self)
        self.get_task_button.setFont(QFont('Courier', 14))
        self.get_task_button.setIcon(QIcon("icons/get_task.png"))
        self.get_task_button.setIconSize(QSize(24, 24))
        self.get_task_button.clicked.connect(self.open_get_task_selection_window)
        self.button_layout.addWidget(self.get_task_button)

        self.stacked_widget = QStackedWidget(self)
        self.layout.addWidget(self.stacked_widget)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.stacked_widget.addWidget(self.main_widget)

    def open_add_task_window(self):
        self.add_task_widget = QWidget()
        layout = QVBoxLayout(self.add_task_widget)

        layout.addWidget(QLabel('Name:', self))
        self.name_entry = QLineEdit(self)
        layout.addWidget(self.name_entry)

        layout.addWidget(QLabel('Tag:', self))
        self.tag_entry = QLineEdit(self)
        layout.addWidget(self.tag_entry)

        layout.addWidget(QLabel('Duration (hours):', self))
        self.duration_entry = QSpinBox(self)
        self.duration_entry.setRange(1, 24)
        layout.addWidget(self.duration_entry)

        layout.addWidget(QLabel('Importance (1-5):', self))
        self.importance_entry = QSpinBox(self)
        self.importance_entry.setRange(1, 5)
        layout.addWidget(self.importance_entry)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        add_button = QPushButton('Add', self)
        add_button.setIcon(QIcon("icons/add.png"))
        add_button.setIconSize(QSize(16, 16))
        add_button.clicked.connect(self.add_task_to_db)
        button_layout.addWidget(add_button)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.setIcon(QIcon("icons/cancel.png"))
        cancel_button.setIconSize(QSize(16, 16))
        cancel_button.clicked.connect(self.go_to_main_window)
        button_layout.addWidget(cancel_button)

        self.stacked_widget.addWidget(self.add_task_widget)
        self.stacked_widget.setCurrentWidget(self.add_task_widget)
        self.animate_transition(self.add_task_widget)

    def add_task_to_db(self):
        name = self.name_entry.text()
        tag = self.tag_entry.text()
        duration = self.duration_entry.value()
        importance = self.importance_entry.value()
        if name and tag:
            database.add_task(name, tag, duration, importance)
            QMessageBox.information(self, "Success", "Task added successfully!")
            self.go_to_main_window()
        else:
            QMessageBox.warning(self, "Error", "Name and Tag fields cannot be empty!")

    def open_get_task_selection_window(self):
        self.get_task_selection_widget = QWidget()
        layout = QVBoxLayout(self.get_task_selection_widget)

        label = QLabel("Select how you want to choose your task:", self)
        layout.addWidget(label)

        tag_button = QPushButton("By Tag", self)
        tag_button.setIcon(QIcon("icons/tag.png"))
        tag_button.setIconSize(QSize(16, 16))
        tag_button.clicked.connect(self.open_get_task_by_tag_window)
        layout.addWidget(tag_button)

        duration_button = QPushButton("By Duration", self)
        duration_button.setIcon(QIcon("icons/duration.png"))
        duration_button.setIconSize(QSize(16, 16))
        duration_button.clicked.connect(self.open_get_task_by_duration_window)
        layout.addWidget(duration_button)

        self.stacked_widget.addWidget(self.get_task_selection_widget)
        self.stacked_widget.setCurrentWidget(self.get_task_selection_widget)
        self.animate_transition(self.get_task_selection_widget)

    def open_get_task_by_tag_window(self):
        self.get_task_by_tag_widget = QWidget()
        layout = QVBoxLayout(self.get_task_by_tag_widget)

        layout.addWidget(QLabel("Enter Tag:", self))
        self.tag_entry = QLineEdit(self)
        layout.addWidget(self.tag_entry)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        ok_button = QPushButton("OK", self)
        ok_button.setIcon(QIcon("icons/ok.png"))
        ok_button.setIconSize(QSize(16, 16))
        ok_button.clicked.connect(self.show_task_by_tag)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.setIcon(QIcon("icons/cancel.png"))
        cancel_button.setIconSize(QSize(16, 16))
        cancel_button.clicked.connect(self.go_to_main_window)
        button_layout.addWidget(cancel_button)

        self.stacked_widget.addWidget(self.get_task_by_tag_widget)
        self.stacked_widget.setCurrentWidget(self.get_task_by_tag_widget)
        self.animate_transition(self.get_task_by_tag_widget)

    def open_get_task_by_duration_window(self):
        self.get_task_by_duration_widget = QWidget()
        layout = QVBoxLayout(self.get_task_by_duration_widget)

        layout.addWidget(QLabel("Enter Time (hours):", self))
        self.time_entry = QSpinBox(self)
        self.time_entry.setRange(1, 24)
        layout.addWidget(self.time_entry)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        ok_button = QPushButton("OK", self)
        ok_button.setIcon(QIcon("icons/ok.png"))
        ok_button.setIconSize(QSize(16, 16))
        ok_button.clicked.connect(self.show_task_by_duration)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.setIcon(QIcon("icons/cancel.png"))
        cancel_button.setIconSize(QSize(16, 16))
        cancel_button.clicked.connect(self.go_to_main_window)
        button_layout.addWidget(cancel_button)

        self.stacked_widget.addWidget(self.get_task_by_duration_widget)
        self.stacked_widget.setCurrentWidget(self.get_task_by_duration_widget)
        self.animate_transition(self.get_task_by_duration_widget)

    def show_task_by_tag(self):
        tag = self.tag_entry.text()
        tasks = database.get_tasks_by_tag(tag)
        if tasks:
            self.display_task_result(tasks)
        else:
            QMessageBox.information(self, "Info", "No tasks found for the given tag.")
            self.go_to_main_window()

    def show_task_by_duration(self):
        time = self.time_entry.value()
        tasks = database.get_tasks_for_duration(time)
        if tasks:
            self.display_task_result(tasks)
        else:
            QMessageBox.information(self, "Info", "No tasks found for the given duration.")
            self.go_to_main_window()

    def display_task_result(self, tasks):
        task = tasks[0]
        self.current_task = task

        self.task_display_widget = QWidget()
        layout = QVBoxLayout(self.task_display_widget)

        task_str = f"Task: {task[0]}\nTag: {task[1]}\nDuration: {task[2]} hours\nImportance: {task[3]}"
        self.task_label = QLabel(task_str, self)
        self.task_label.setFont(QFont('Courier', 14))
        self.task_label.setWordWrap(True)
        layout.addWidget(self.task_label)

        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)

        done_button = QPushButton("Done", self)
        done_button.setIcon(QIcon("icons/done.png"))
        done_button.setIconSize(QSize(16, 16))
        done_button.clicked.connect(self.task_done)
        button_layout.addWidget(done_button)

        delete_button = QPushButton("Delete", self)
        delete_button.setIcon(QIcon("icons/delete.png"))
        delete_button.setIconSize(QSize(16, 16))
        delete_button.clicked.connect(self.delete_task)
        button_layout.addWidget(delete_button)

        self.stacked_widget.addWidget(self.task_display_widget)
        self.stacked_widget.setCurrentWidget(self.task_display_widget)
        self.animate_transition(self.task_display_widget)

    def task_done(self):
        self.current_task = None
        self.go_to_main_window()

    def delete_task(self):
        if self.current_task:
            database.delete_task(self.current_task[0])
            QMessageBox.information(self, "Info", "Task deleted successfully!")
            self.current_task = None
            self.go_to_main_window()

    def go_to_main_window(self):
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.animate_transition(self.main_widget)

    def animate_transition(self, target_widget):
        current_index = self.stacked_widget.currentIndex()
        target_index = self.stacked_widget.indexOf(target_widget)

        if current_index != target_index:
            animation = QPropertyAnimation(self.stacked_widget, b"pos")
            animation.setDuration(300)
            animation.setStartValue(self.stacked_widget.pos())
            animation.setEndValue(self.stacked_widget.pos())
            animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TheOrganizationApp()
    window.show()
    sys.exit(app.exec_())
