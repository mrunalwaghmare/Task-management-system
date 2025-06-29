# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 16:58:54 2024

@author: Mrunal
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 16:26:13 2024

@author: Mrunal
"""

import sqlite3
from customtkinter import *
from tkinter import ttk, messagebox, Spinbox
from PIL import Image, ImageTk
import tkinter as tk

set_appearance_mode('dark')
set_default_color_theme("blue")

# Main window
root = CTk()
root.geometry("600x700")
root.title("TO DO")

# Load and display the background image
image2 = Image.open(r"D:\python practi\tm.jpg")
image2 = image2.resize((400, 400), Image.ANTIALIAS) 
 # This line will generate a DeprecationWarning
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.image = background_image
background_label.place(x=800, y=0)


def connect_db():
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS todo(
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Task TEXT,
        Category TEXT,
        Time INTEGER,
        Status TEXT
        )""")
    conn.commit()
    conn.close()
connect_db()

todo_table = ttk.Treeview(root)

def insert_task(task, category, time, status):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO todo (Task, Category, Time, Status) VALUES (?,?,?,?)", 
                (task, category, time, status))
    conn.commit()
    conn.close()
    view_task()

def update_task(id, task, category, time, status):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("UPDATE todo SET Task=?, Category=?, Time=?, Status=? WHERE Id=?", 
                (task, category, time, status, id))
    conn.commit()
    conn.close()
    view_task()

def delete_task(id):
    conn = sqlite3.connect("todo.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM todo WHERE Id=?", (id,))
    conn.commit()
    conn.close()
    view_task()

def view_task(search_term=""):
    conn = sqlite3.connect('todo.db')
    cur = conn.cursor()
    if search_term:
        cur.execute("SELECT * FROM todo WHERE Task LIKE ?", ('%' + search_term + '%',))
    else:
        cur.execute("SELECT * FROM todo")
    rows = cur.fetchall()
    conn.close()

    for row in todo_table.get_children():
        todo_table.delete(row)

    for row in rows:
        todo_table.insert("", END, values=row)

def add_task():
    insert_task(task_entry.get(), imp_entry.get(), time_spinbox.get(), status_entry.get())
    task_entry.delete(0, END)
    imp_entry.delete(0, END)
    time_spinbox.delete(0, END)
    status_entry.delete(0, END)

def update_selected_task():
    selected = todo_table.focus()
    if not selected:
        messagebox.showwarning("UPDATE todo", "Select a task to update")
        return

    values = todo_table.item(selected, 'values')
    update_task(values[0], task_entry.get(), imp_entry.get(), time_spinbox.get(), status_entry.get())

    task_entry.delete(0, END)
    imp_entry.delete(0, END)
    time_spinbox.delete(0, END)
    status_entry.delete(0, END)

def delete_selected_task():
    selected = todo_table.focus()
    if not selected:
        messagebox.showwarning("Delete Task", "Select a task to delete")
        return

    values = todo_table.item(selected, 'values')
    delete_task(values[0])

    task_entry.delete(0, END)
    imp_entry.delete(0, END)
    time_spinbox.delete(0, END)
    status_entry.delete(0, END)

def get_selected_task(event):
    selected = todo_table.focus()
    if not selected:
        return

    values = todo_table.item(selected, 'values')
    task_entry.delete(0, END)
    task_entry.insert(END, values[1])

    imp_entry.delete(0, END)
    imp_entry.insert(END, values[2])

    time_spinbox.delete(0, END)
    time_spinbox.insert(0, values[3])

    status_entry.delete(0, END)
    status_entry.insert(END, values[4])

def search_task():
    search_term = search_entry.get()
    view_task(search_term)

label = CTkLabel(master=root, text="TASK MANAGEMENT SYSTEM", font=("Arial", 25, "bold"))
label.place(x=40, y=40)

label = CTkLabel(master=root, text="Write your task here", width=20, height=1, font=("Arial", 17, "bold"))
label.place(x=50, y=200)
task_entry = CTkEntry(master=root, placeholder_text="Add your task here", text_color="#FFCC70")
task_entry.place(x=250, y=200)

label = CTkLabel(master=root, text="Important or not", width=20, height=1, font=("Arial", 17, "bold"))
label.place(x=50, y=240)
imp_entry = CTkEntry(master=root, placeholder_text="important or not", text_color="#FFCC70")
imp_entry.place(x=250, y=240)

label = CTkLabel(master=root, text="Time required", width=20, height=1, font=("Arial", 17, "bold"))
label.place(x=50, y=280)
time_spinbox = Spinbox(root, from_=0, to=100, increment=1, width=5)
time_spinbox.place(x=250, y=280)

label = CTkLabel(master=root, text="Add status completed or not", width=20, height=1, font=("Arial", 17, "bold"))
label.place(x=50, y=320)
status_entry = CTkEntry(master=root, placeholder_text="complete/not", text_color="#FFCC70")
status_entry.place(x=280, y=320)

add_button = CTkButton(master=root, text="Add Task", hover_color='#4158D0',
                       border_color='#ffcc70', border_width=2, command=add_task, fg_color="transparent")
add_button.place(x=20, y=90)

update_button = CTkButton(master=root, text="Update Task", hover_color='#4158D0',
                          border_color='#FFCC70', border_width=2, command=update_selected_task, fg_color="transparent")
update_button.place(x=170, y=90)

del_button = CTkButton(master=root, text="Delete Task", hover_color='#4158D0',
                       border_color='#FFCC70', border_width=2, command=delete_selected_task, fg_color="transparent")
del_button.place(x=320, y=90)

search_label = CTkLabel(master=root, text="Search Task", width=20, height=1, font=("Arial", 17, "bold"))
search_label.place(x=50, y=400)
search_entry = CTkEntry(master=root, placeholder_text="Search task", text_color="#FFCC70")
search_entry.place(x=250, y=400)
search_button = CTkButton(master=root, text="Search", hover_color='#4158D0',
                          border_color='#FFCC70', border_width=2, command=search_task, fg_color="transparent")
search_button.place(x=400, y=400)

def windo():
    root.destroy()

d3 = CTkButton(master=root, text='exit', command=windo, border_width=2, hover_color='#4158D0',
               fg_color="transparent", border_color='#FFCC70',)
d3.place(x=470, y=90)

columns = ('id', 'task', 'imp', 'time', 'status')
todo_table = ttk.Treeview(root, columns=columns, show='headings')
todo_table.heading("id", text="ID")
todo_table.heading("task", text="Task")
todo_table.heading("time", text="Time")
todo_table.heading("imp", text="Category")
todo_table.heading("status", text="Status")
style = ttk.Style()
style.configure("Treeview.Heading", background="#d3d3d3", foreground="black", font=('Arial', 10, 'bold'))
style.configure("Treeview", background="#f0f0f0", foreground="black", fieldbackground="#f0f0f0", font=('Arial', 10))
style.map("Treeview", background=[('selected', '#3a3a3a')])

todo_table.place(x=30, y=450)

todo_table.bind("<ButtonRelease-1>", get_selected_task)

view_task()

root.mainloop()
