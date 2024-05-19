import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit,
    QSpinBox, QMessageBox, QStackedWidget, QTableWidget, QTableWidgetItem,
    QListWidget, QListWidgetItem, QInputDialog, QCalendarWidget, QFrame,QHeaderView
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QMovie
import database  # assuming the database code is saved in a file named 'database.py'


class TheAstronautApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Astronaut")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #202020; color: #ffffff;")

        self.stacked_widget = QStackedWidget()
        self.initUI()
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stacked_widget)

        self.daily_tasks = []  # List to store daily tasks

        database.create_tables()
        self.load_daily_plan_data()

    def initUI(self):
        self.create_welcome_page()
        self.create_add_task_page()
        self.create_get_task_selection_page()
        self.create_daily_plan_page()
        self.create_set_goals_page()

        self.stacked_widget.setCurrentWidget(self.welcome_widget)

    def create_back_button(self):
        back_button = QLabel("← Back", self)
        back_button.setFont(QFont('Courier New', 14))
        back_button.setStyleSheet("color: #00ace6;")
        back_button.mousePressEvent = self.go_to_main_window
        back_button.setCursor(Qt.PointingHandCursor)
        return back_button

    def create_welcome_page(self):
        self.welcome_widget = QWidget()
        layout = QVBoxLayout(self.welcome_widget)
        layout.setAlignment(Qt.AlignCenter)
        gif_label = QLabel(self)
        movie = QMovie(r"C:\Users\amir\Documents\GitHub\Python-Advance\The ORGENIZER\astronout\SQie.gif")
        gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(gif_label)

        title = QLabel("Welcome to The Astronaut", self)
        title.setFont(QFont('Courier New', 24))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        options = [("Add Task", self.open_add_task_page),
                   ("Get Task", self.open_get_task_selection_page),
                   ("Daily Plan", self.open_daily_plan_page),
                   ("Set Goals", self.open_set_goals_page)]

        for text, method in options:
            label = QLabel(text, self)
            label.setFont(QFont('Courier New', 18))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #00ace6;")
            label.mousePressEvent = lambda event, method=method: method()
            label.setCursor(Qt.PointingHandCursor)
            label.installEventFilter(self)
            layout.addWidget(label)

        self.stacked_widget.addWidget(self.welcome_widget)

    def create_add_task_page(self):
        self.add_task_widget = QWidget()
        layout = QVBoxLayout(self.add_task_widget)

        title = QLabel("Add Task", self)
        title.setFont(QFont('Courier New', 24))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        back_button = self.create_back_button()
        layout.addWidget(back_button)

        self.name_entry = QLineEdit(self)
        self.name_entry.setPlaceholderText("Task Name")
        layout.addWidget(self.name_entry)

        self.tag_entry = QLineEdit(self)
        self.tag_entry.setPlaceholderText("Tag")
        layout.addWidget(self.tag_entry)

        self.duration_entry = QSpinBox(self)
        self.duration_entry.setRange(1, 24)
        self.duration_entry.setPrefix("Duration (hours): ")
        layout.addWidget(self.duration_entry)

        self.importance_entry = QSpinBox(self)
        self.importance_entry.setRange(1, 5)
        self.importance_entry.setPrefix("Importance: ")
        layout.addWidget(self.importance_entry)

        button_layout = QHBoxLayout()
        add_button = QPushButton('Add', self)
        add_button.clicked.connect(self.add_task)
        button_layout.addWidget(add_button)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.clicked.connect(self.go_to_main_window)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.stacked_widget.addWidget(self.add_task_widget)

    def create_get_task_selection_page(self):
        self.get_task_selection_widget = QWidget()
        layout = QVBoxLayout(self.get_task_selection_widget)

        title = QLabel("Get Task", self)
        title.setFont(QFont('Courier New', 24))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        back_button = self.create_back_button()
        layout.addWidget(back_button)

        self.tag_selection_label = QLabel('Get Task by Tag', self)
        self.tag_selection_label.setFont(QFont('Courier New', 18))
        self.tag_selection_label.setAlignment(Qt.AlignCenter)
        self.tag_selection_label.setStyleSheet("color: #00ace6;")
        self.tag_selection_label.mousePressEvent = self.get_task_by_tag
        self.tag_selection_label.setCursor(Qt.PointingHandCursor)
        self.tag_selection_label.installEventFilter(self)
        layout.addWidget(self.tag_selection_label)

        self.duration_selection_label = QLabel('Get Task by Duration', self)
        self.duration_selection_label.setFont(QFont('Courier New', 18))
        self.duration_selection_label.setAlignment(Qt.AlignCenter)
        self.duration_selection_label.setStyleSheet("color: #00ace6;")
        self.duration_selection_label.mousePressEvent = self.get_task_by_duration
        self.duration_selection_label.setCursor(Qt.PointingHandCursor)
        self.duration_selection_label.installEventFilter(self)
        layout.addWidget(self.duration_selection_label)

        self.stacked_widget.addWidget(self.get_task_selection_widget)

    def create_daily_plan_page(self):
        self.daily_plan_widget = QWidget()
        layout = QVBoxLayout(self.daily_plan_widget)

        title_layout = QHBoxLayout()
        self.date_label = QLabel(QDate.currentDate().toString("yyyy-MM-dd"), self)
        self.date_label.setFont(QFont('Courier New', 18))
        title_layout.addWidget(self.date_label)

        layout.addLayout(title_layout)

        self.daily_table = QTableWidget(24, 2)
        self.daily_table.setHorizontalHeaderLabels(['Hour', 'Task'])
        self.daily_table.verticalHeader().setVisible(False)
        header = self.daily_table.horizontalHeader()
        header.setStyleSheet("color: #ffffff;")
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Resize hour column to fit content
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Stretch the task column
        header.setDefaultSectionSize(150)  # Set default section size for better visibility
        self.daily_table.setStyleSheet("QHeaderView::section { background-color: #2e2e2e; }")  # Set header background color
        for i in range(24):
            self.daily_table.setItem(i, 0, QTableWidgetItem(f"{i}:00 - {i + 1}:00"))
        layout.addWidget(self.daily_table)

        button_layout = QHBoxLayout()
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_daily_plan)
        button_layout.addWidget(save_button)

        back_button = self.create_back_button()
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)

        self.stacked_widget.addWidget(self.daily_plan_widget)
    def load_daily_plan_data(self):
        # Fetch data from the daily_plan database table and fill the daily plan table
        date_str = self.date_label.text()
        date = QDate.fromString(date_str, "yyyy-MM-dd").toString("yyyy-MM-dd")
        tasks = database.get_daily_plan(date)
        for task in tasks:
            hour = task[2]
            task_name = task[3]
            item = QTableWidgetItem(task_name)
            self.daily_table.setItem(hour, 1, item)


    def create_set_goals_page(self):
        self.set_goals_widget = QWidget()
        layout = QVBoxLayout(self.set_goals_widget)

        title = QLabel("Set Goals", self)
        title.setFont(QFont('Courier New', 24))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        back_button = self.create_back_button()
        layout.addWidget(back_button)

        self.goal_entry = QLineEdit(self)
        self.goal_entry.setPlaceholderText("Enter your goal")
        layout.addWidget(self.goal_entry)

        button_layout = QHBoxLayout()
        add_button = QPushButton('Add Goal', self)
        add_button.clicked.connect(self.add_goal)
        button_layout.addWidget(add_button)

        delete_button = QPushButton('Delete Goal', self)
        delete_button.clicked.connect(self.delete_goal)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        self.goals_list = QListWidget(self)
        layout.addWidget(self.goals_list)

        self.stacked_widget.addWidget(self.set_goals_widget)
        self.load_goals()

    def add_task(self):
        name = self.name_entry.text()
        tag = self.tag_entry.text()
        duration = self.duration_entry.value()
        importance = self.importance_entry.value()

        if name and tag:
            database.add_task(name, tag, duration, importance)
            QMessageBox.information(self, "Success", "Task added successfully!")
            self.go_to_main_window()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def get_task_by_tag(self, event):
        tag, ok = QInputDialog.getText(self, 'Get Task by Tag', 'Enter the tag:')
        if ok and tag:
            tasks = database.get_tasks_by_tag(tag)
            if tasks:
                self.show_task(tasks[0])
            else:
                QMessageBox.information(self, "No Tasks", "No tasks found with this tag.")

    def get_task_by_duration(self, event):
        duration, ok = QInputDialog.getInt(self, 'Get Task by Duration', 'Enter duration (hours):')
        if ok:
            tasks = database.get_tasks_for_duration(duration)
            if tasks:
                self.show_task(tasks[0])
            else:
                QMessageBox.information(self, "No Tasks", "No tasks found for this duration.")

    def show_task(self, task):
        self.current_task = task
        task_widget = QWidget()
        layout = QVBoxLayout(task_widget)

        task_name = QLabel(f"Task: {task[1]}", self)
        task_name.setFont(QFont('Courier New', 18))
        layout.addWidget(task_name)

        task_tag = QLabel(f"Tag: {task[2]}", self)
        task_tag.setFont(QFont('Courier New', 18))
        layout.addWidget(task_tag)

        task_duration = QLabel(f"Duration: {task[3]} hours", self)
        task_duration.setFont(QFont('Courier New', 18))
        layout.addWidget(task_duration)

        task_importance = QLabel(f"Importance: {task[4]}", self)
        task_importance.setFont(QFont('Courier New', 18))
        layout.addWidget(task_importance)

        button_layout = QHBoxLayout()
        done_button = QPushButton('Not Done', self)
        button_layout.addWidget(done_button)

        delete_button = QPushButton('Done', self)
        delete_button.clicked.connect(self.delete_current_task)
        delete_button.clicked.connect(self.complete_task)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        self.stacked_widget.addWidget(task_widget)
        self.stacked_widget.setCurrentWidget(task_widget)

    def complete_task(self):
        QMessageBox.information(self, "Task Completed", "Task marked as completed!")
        self.go_to_main_window()

    def delete_current_task(self):
        task_id = self.current_task[0]
        database.delete_task(task_id)
        QMessageBox.information(self, "Task Deleted", "Task has been deleted.")
        self.go_to_main_window()

    def save_daily_plan(self):
        date_str = self.date_label.text()
        date = QDate.fromString(date_str, "yyyy-MM-dd").toString("yyyy-MM-dd")
        for i in range(24):
            task_item = self.daily_table.item(i, 1)
            if task_item:
                task_name = task_item.text()
                # Here, we assume task_id is not applicable for daily plan tasks
                self.daily_tasks.append(task_name)  # Add task to daily_tasks list
                database.add_daily_plan(date, i, task_name)  # Save to database
        QMessageBox.information(self, "Daily Plan Saved", "Your daily plan has been saved.")
        self.go_to_main_window()
    def add_goal(self):
        goal = self.goal_entry.text()
        if goal:
            database.add_goal(goal)
            self.goal_entry.clear()
            self.load_goals()
            QMessageBox.information(self, "Goal Added", "Your goal has been added.")

    def delete_goal(self):
        selected_item = self.goals_list.currentItem()
        if selected_item:
            goal_id = selected_item.data(Qt.UserRole)
            database.delete_goal(goal_id)
            self.load_goals()
            QMessageBox.information(self, "Goal Deleted", "Your goal has been deleted.")
        else:
            QMessageBox.warning(self, "Error", "Please select a goal to delete.")

    def load_goals(self):
        self.goals_list.clear()
        goals = database.get_goals()
        for goal in goals:
            item = QListWidgetItem(goal[1])
            item.setData(Qt.UserRole, goal[0])
            self.goals_list.addItem(item)

    def go_to_main_window(self, event=None):
        self.stacked_widget.setCurrentWidget(self.welcome_widget)

    def get_task_id_by_name(self, task_name):
        tasks = database.get_tasks_by_tag("")
        for task in tasks:
            if task[1] == task_name:
                return task[0]
        return None


    def eventFilter(self, obj, event):
        if event.type() == event.Enter:
            obj.setStyleSheet("color: #00ffff;")
        elif event.type() == event.Leave:
            obj.setStyleSheet("color: #00ace6;")
        return super().eventFilter(obj, event)

    def open_add_task_page(self):
        self.stacked_widget.setCurrentWidget(self.add_task_widget)

    def open_get_task_selection_page(self):
        self.stacked_widget.setCurrentWidget(self.get_task_selection_widget)

    def open_daily_plan_page(self):
        self.stacked_widget.setCurrentWidget(self.daily_plan_widget)

    def open_set_goals_page(self):
        self.stacked_widget.setCurrentWidget(self.set_goals_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TheAstronautApp()
    ex.show()
    sys.exit(app.exec_())