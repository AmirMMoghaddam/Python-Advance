import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import database

class TheOrganizationApp:
    def __init__(self, root):
        self.root = root
        self.style = Style('darkly')  # Apply a dark theme from ttkbootstrap
        self.root.title("The Organization")
        self.root.geometry("800x500")
        self.root.configure(bg='#2b2b2b')  # Ensure the background is consistent

        self.current_task = None
        self.sidebar = None  # Sidebar will be dynamically created
        self.create_main_window()

    def create_main_window(self):
        # Clear the existing widgets before creating the main window
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_label = tk.Label(main_frame, text="The Organization", font=('Helvetica', 24, 'bold'), fg='#ffffff', bg='#2b2b2b')
        header_label.pack(pady=50)

        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(pady=10)

        self.add_task_button = ttk.Button(button_frame, text="Add Task", command=self.open_add_task_window, style="TButton")
        self.add_task_button.pack(side=tk.LEFT, padx=10)

        self.get_task_button = ttk.Button(button_frame, text="Get Task", command=self.open_get_task_selection_window, style="TButton")
        self.get_task_button.pack(side=tk.RIGHT, padx=10)

    def create_sidebar(self, task_str):
        self.sidebar = tk.Frame(self.root, bg='#1c1c1c', width=250, height=500, padx=10, pady=10)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        header_label = tk.Label(self.sidebar, text="Current Task", font=('Helvetica', 16, 'bold'), fg='#ffffff', bg='#1c1c1c')
        header_label.pack(pady=20)

        self.task_label = tk.Label(self.sidebar, text=task_str, font=('Helvetica', 14), fg='#ffffff', bg='#1c1c1c', wraplength=200)
        self.task_label.pack(pady=10)

        button_frame = tk.Frame(self.sidebar, bg='#1c1c1c')
        button_frame.pack(pady=20)

        done_button = ttk.Button(button_frame, text="Done", command=self.task_done, style="TButton")
        done_button.pack(side=tk.LEFT, padx=10)

        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_task, style="TButton")
        delete_button.pack(side=tk.RIGHT, padx=10)

    def open_add_task_window(self):
        self.add_task_window = tk.Toplevel(self.root)
        self.add_task_window.title("Add Task")
        self.add_task_window.geometry("350x400")
        self.add_task_window.configure(bg='#2b2b2b')

        self.create_add_task_widgets(self.add_task_window)

    def create_add_task_widgets(self, window):
        ttk.Label(window, text="Name:", style="TLabel").pack(pady=5)
        self.name_entry = ttk.Entry(window, style="TEntry")
        self.name_entry.pack(pady=5)

        ttk.Label(window, text="Tag:", style="TLabel").pack(pady=5)
        self.tag_entry = ttk.Entry(window, style="TEntry")
        self.tag_entry.pack(pady=5)

        ttk.Label(window, text="Duration (hours):", style="TLabel").pack(pady=5)
        self.duration_entry = ttk.Entry(window, style="TEntry")
        self.duration_entry.pack(pady=5)

        ttk.Label(window, text="Importance (1-5):", style="TLabel").pack(pady=5)
        self.importance_entry = ttk.Entry(window, style="TEntry")
        self.importance_entry.pack(pady=5)

        button_frame = tk.Frame(window, bg='#2b2b2b')
        button_frame.pack(pady=20)

        add_button = ttk.Button(button_frame, text="Add", command=self.add_task_to_db, style="TButton")
        add_button.pack(side=tk.LEFT, padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=window.destroy, style="TButton")
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def add_task_to_db(self):
        name = self.name_entry.get()
        tag = self.tag_entry.get()
        duration = self.duration_entry.get()
        importance = self.importance_entry.get()
        database.add_task(name, tag, duration, importance)
        messagebox.showinfo("Info", "Task added successfully!")
        self.add_task_window.destroy()

    def open_get_task_selection_window(self):
        self.get_task_selection_window = tk.Toplevel(self.root)
        self.get_task_selection_window.title("Select Task Criteria")
        self.get_task_selection_window.geometry("300x200")
        self.get_task_selection_window.configure(bg='#2b2b2b')

        ttk.Label(self.get_task_selection_window, text="Select how you want to choose your task:", style="TLabel").pack(pady=10)

        tag_button = ttk.Button(self.get_task_selection_window, text="By Tag", command=self.open_get_task_by_tag_window, style="TButton")
        tag_button.pack(pady=10)

        duration_button = ttk.Button(self.get_task_selection_window, text="By Duration", command=self.open_get_task_by_duration_window, style="TButton")
        duration_button.pack(pady=10)

    def open_get_task_by_tag_window(self):
        self.get_task_selection_window.destroy()

        self.get_task_by_tag_window = tk.Toplevel(self.root)
        self.get_task_by_tag_window.title("Get Task by Tag")
        self.get_task_by_tag_window.geometry("300x150")
        self.get_task_by_tag_window.configure(bg='#2b2b2b')

        ttk.Label(self.get_task_by_tag_window, text="Enter Tag:", style="TLabel").pack(pady=5)
        self.tag_entry = ttk.Entry(self.get_task_by_tag_window, style="TEntry")
        self.tag_entry.pack(pady=5)

        button_frame = tk.Frame(self.get_task_by_tag_window, bg='#2b2b2b')
        button_frame.pack(pady=20)

        ok_button = ttk.Button(button_frame, text="OK", command=self.show_task_by_tag, style="TButton")
        ok_button.pack(side=tk.LEFT, padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.get_task_by_tag_window.destroy, style="TButton")
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def open_get_task_by_duration_window(self):
        self.get_task_selection_window.destroy()

        self.get_task_by_duration_window = tk.Toplevel(self.root)
        self.get_task_by_duration_window.title("Get Task by Duration")
        self.get_task_by_duration_window.geometry("300x150")
        self.get_task_by_duration_window.configure(bg='#2b2b2b')

        ttk.Label(self.get_task_by_duration_window, text="Enter Time (hours):", style="TLabel").pack(pady=5)
        self.time_entry = ttk.Entry(self.get_task_by_duration_window, style="TEntry")
        self.time_entry.pack(pady=5)

        button_frame = tk.Frame(self.get_task_by_duration_window, bg='#2b2b2b')
        button_frame.pack(pady=20)

        ok_button = ttk.Button(button_frame, text="OK", command=self.show_task_by_duration, style="TButton")
        ok_button.pack(side=tk.LEFT, padx=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.get_task_by_duration_window.destroy, style="TButton")
        cancel_button.pack(side=tk.RIGHT, padx=10)

    def show_task_by_tag(self):
        tag = self.tag_entry.get()
        tasks = database.get_tasks_by_tag(tag)
        self.get_task_by_tag_window.destroy()

        self.show_task_result(tasks)

    def show_task_by_duration(self):
        time = int(self.time_entry.get())
        tasks = database.get_tasks_for_duration(time)
        self.get_task_by_duration_window.destroy()

        self.show_task_result(tasks)

    def show_task_result(self, tasks):
        # Clear the existing widgets before showing task result
        for widget in self.root.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.root, bg='#2b2b2b', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        if tasks:
            task = tasks[0]
            self.current_task = task  # Store the current task for deletion
            task_str = f"Task: {task[0]}\nTag: {task[1]}\nDuration: {task[2]} hours\nImportance: {task[3]}"
            self.create_sidebar(task_str)
        else:
            messagebox.showinfo("Info", "No tasks available for the given criteria.")
            self.create_main_window()

    def task_done(self):
        self.current_task = None
        self.sidebar.destroy()  # Remove the sidebar
        self.create_main_window()

    def delete_task(self):
        if self.current_task:
            database.delete_task(self.current_task[0])  # Delete task by its ID
            messagebox.showinfo("Info", "Task deleted successfully!")
            self.current_task = None
            self.sidebar.destroy()  # Remove the sidebar
            self.create_main_window()

if __name__ == "__main__":
    root = tk.Tk()
    app = TheOrganizationApp(root)
    root.mainloop()
