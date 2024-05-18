import mysql.connector
from mysql.connector import errorcode
import re

def connect_to_db():
    return mysql.connector.connect(
        host = "localhost",
        user= "root",
        password="p@sswordis1379",
        database = "organization"
    )
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
    cursor.execute("DELETE FROM tasks WHERE task_name = %s", (task_id,))
    conn.commit()
    conn.close()