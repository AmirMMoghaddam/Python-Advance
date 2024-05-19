import mysql.connector
from mysql.connector import errorcode

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="p@sswordis1379",
        database="organization"
    )

def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()
    
    # Create tasks table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        tag VARCHAR(255),
        duration INT,
        importance INT
    )
    """)
    
    # Create daily_plan table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_plan (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE NOT NULL,
        hour INT NOT NULL,
        task_name VARCHAR(255)
    )
    """)

    # Create goals table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INT AUTO_INCREMENT PRIMARY KEY,
        goal TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

def add_task(name, tag, duration, importance):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task_name, tag, duration, importance) VALUES (%s, %s, %s, %s)", (name, tag, duration, importance))
    conn.commit()
    conn.close()

def get_tasks_for_duration(duration):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE duration <= %s ORDER BY importance DESC", (duration,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_tasks_by_tag(tag):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE tag = %s ORDER BY importance DESC", (tag,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def delete_task(task_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
    conn.commit()
    conn.close()

def add_daily_plan(date, hour, task_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO daily_plan (date, hour, task_name) VALUES (%s, %s, %s)", (date, hour, task_name))
    conn.commit()
    conn.close()
    
def get_daily_plan(date):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_plan WHERE date = %s", (date,))
    daily_plan = cursor.fetchall()
    conn.close()
    return daily_plan

def add_goal(goal):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO goals (goal) VALUES (%s)", (goal,))
    conn.commit()
    conn.close()

def get_goals():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals")
    goals = cursor.fetchall()
    conn.close()
    return goals

def delete_goal(goal_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE goal_id = %s", (goal_id,))
    conn.commit()
    conn.close()
