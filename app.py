import sqlite3
import sys
import os
import time
from datetime import datetime

if 'idlelib.run' in sys.modules:
    inIdle = True
else:
    inIdle = False


def buildCursor():
    global conn
    conn = sqlite3.connect('database.db')
    global cursor
    cursor = conn.cursor()


def cls():
    global inIdle
    if inIdle == False:
        os.system('cls' if os.name == 'nt' else 'clear')
    else:
        print("-" * 40)


def inputData():
    task_or_todo = input("Choose: [Reminder][Todo]")
    if (task_or_todo.lower()).strip() == "todo" or (task_or_todo.lower()).strip() == "t":
        todo = Todo()
        todo.update_name()
        todo.update_priority()
        todo.update_db()
    elif (task_or_todo.lower()).strip() == "reminder" or (task_or_todo.lower()).strip() == "r":
        reminder = Reminder()
        reminder.update_name()
        reminder.update_priority()
        reminder.update_expire_date()
        reminder.update_db()
    else:
        print("Invalid Input")


def viewData():
    list1 = []
    sql = "select * from todoList"
    data = cursor.execute(sql)
    for task in data.fetchall():
        list1.append(task)
    for item in list1:
        v_type = item[0]
        v_task = item[1]
        v_priority = item[2]
        v_completed = item[3]
        v_expire_date = item[4]
        if v_completed == 0:
            v_completed = "No"
        elif v_completed == 1:
            v_completed = "Yes"
        else:
            v_completed = "ERROR"

        print("----------")
        print("Type:", v_type)
        print("Task:", v_task)
        print("Priority:", v_priority)
        print("Completed:", v_completed)
        if v_expire_date:
            print("Expire date:", v_expire_date)

    print("----------")


def modifyData():
    task = input("Which task do you want to modify? ")
    to_modify = input("What do you want to modify? [name, priority, completed]")
    if (to_modify.lower()).strip() == "name" or (to_modify.lower()).strip() == "n":
        new_text = input("New Name: ")
        cursor.execute("""UPDATE todoList SET task = ? WHERE task = ?""", (new_text, task))
    elif (to_modify.lower()).strip() == "priority" or (to_modify.lower()).strip() == "p":
        new_priority = input("New Priority: ")
        cursor.execute("""UPDATE todoList SET priority = ? WHERE task = ?""", (new_priority, task))
    elif (to_modify.lower()).strip() == "completed" or (to_modify.lower()).strip() == "c":
        new_completed_pre = input("Completed? [yes][no] ")
        if new_completed_pre.lower() == "yes":
            new_completed = 1
        elif new_completed_pre.lower() == "no":
            new_completed = 0
        else:
            print("Invalid Input")
        cursor.execute("""UPDATE todoList SET completed = ? WHERE task = ?""", (new_completed, task))
    else:
        print("Invalid Input")
    conn.commit()
    cls()


def removeData():
    task = input("Which task do you want to delete? ")
    cursor.execute("""DELETE FROM todoList WHERE task=?""", (task,))
    conn.commit()
    cls()


def initDatabase():
    buildCursor()
    try:
        sql = '''create table todoList (
            type text,
            task text,
            priority int,
            completed bool,
            expire_date text
        )'''
        cursor.execute(sql)
        print("Database setup invalid, building...")
    except:
        print("Database setup valid, continuing...")

    print('Running in IDLE' if 'idlelib.run' in sys.modules else 'Not running in IDLE')

    time.sleep(.75)
    cls()


class Todo:
    def __init__(self, completed=False, priority=0, task="New Task"):
        self.completed = completed
        self.priority = priority
        self.task = task

    def update_name(self):
        task = input('Task: ')
        self.task = task

    def update_priority(self):
        priority = input('Priority: ')
        self.priority = priority

    def update_completed(self, completed):
        self.completed = completed

    def update_db(self):
        sql = ''' INSERT INTO todoList
                          (type, task, priority, completed)
                          VALUES (:st_type, :st_task, :st_priority, :st_completed)'''
        cursor.execute(sql, {
            'st_type': 'TODO',
            'st_task': self.task,
            'st_priority': self.priority,
            'st_completed': self.completed
        })
        conn.commit()
        cls()


class Reminder(Todo):
    def __init__(self, completed=False, priority=0, task="New Task", expire_date=datetime.today()):
        super().__init__(completed, priority, task)
        self.expire_date = expire_date

    def update_expire_date(self):
        expire_date = input('Expire date: YYYY-MM-DD')
        self.expire_date = datetime.strptime(expire_date, '%Y-%m-%d')

    def update_db(self):
        sql = ''' INSERT INTO todoList
                          (type, task, priority, completed, expire_date)
                          VALUES (:st_type, :st_task, :st_priority, :st_completed, :st_expire)'''
        cursor.execute(sql, {
            'st_type': 'REMINDER',
            'st_task': self.task,
            'st_priority': self.priority,
            'st_completed': self.completed,
            'st_expire': self.expire_date
        })
        conn.commit()
        cls()

# Start
run = True
initDatabase()

while run:
    print("==== TODO LIST ====")
    viewData()
    control = input("Please select an option. [Input][View][Modify][Remove][Exit]: ")
    if (control.lower()).strip() == "input" or (control.lower()).strip() == "i":
        inputData()
    elif (control.lower()).strip() == "view" or (control.lower()).strip() == "v":
        viewData()
    elif (control.lower()).strip() == "modify" or (control.lower()).strip() == "m":
        modifyData()
    elif (control.lower()).strip() == "remove" or (control.lower()).strip() == "r":
        removeData()
    elif (control.lower()).strip() == "exit" or (control.lower()).strip() == "e":
        run = False
    else:
        print("Invalid Input")
        time.sleep(1)
