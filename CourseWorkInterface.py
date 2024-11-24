from tkinter import *
from tkinter import ttk
from sqlite3 import *

connection = connect("C:/Users/Даниил/Desktop/Курсовая работа/CourseWorkFullDB.db")
cursor = connection.cursor()

main_window = Tk()
main_window.title("Успеваемость учащихся")
main_window.geometry("1280x720")
main_window.resizable(False, False)

student_columns = ("ID", "Full_name", "Birth_date", "Study_class", "Student_photo")

database_viewport = ttk.Treeview(main_window, show="headings", columns=student_columns)

database_viewport.heading("ID", text="№")
database_viewport.heading("Full_name", text="ФИО")
database_viewport.heading("Birth_date", text="Дата рождения")
database_viewport.heading("Study_class", text="Класс, группа")
database_viewport.heading("Student_photo", text="Фото")

database_viewport.grid(row=0, column=0, sticky=NW)

def add_student_data_to_database():

    def add_entry_to_student_table():
        one_student_data = [name_entry.get(), date_entry.get(), class_entry.get()]
        cursor.execute("""
            INSERT INTO Student
            ('Full_name', 'Birth_date', 'Study_class')   
            VALUES
            (?, ?, ?)""", one_student_data)
        connection.commit()

    add_window = Tk()
    add_window.title("Добавить ученика")
    add_window.geometry("400x300")
    add_window.resizable(False, False)

    name_label = ttk.Label(add_window, text="ФИО")
    name_label.grid(row=0, column=0, sticky=NW, padx=20)
    date_label = ttk.Label(add_window, text="Дата рождения")
    date_label.grid(row=0, column=1, sticky=N, padx=30)
    class_label = ttk.Label(add_window, text="Класс, группа")
    class_label.grid(row=0, column=2, sticky=NE, padx=20)

    name_entry = ttk.Entry(add_window)
    name_entry.grid(row=1, column=0)
    date_entry = ttk.Entry(add_window)
    date_entry.grid(row=1, column=1)
    class_entry = ttk.Entry(add_window)
    class_entry.grid(row=1, column=2)

    add_button = ttk.Button(add_window, text="Добавить", command=add_entry_to_student_table)
    add_button.grid(row=2, column=1)

def refresh_viewport_data_with_student():
    cursor.execute("SELECT * FROM Student")
    student_rows = cursor.fetchall()

    for i in database_viewport.get_children():
        database_viewport.delete(i)

    for row in student_rows:
        database_viewport.insert("", END, values=row)

add_button = ttk.Button(main_window, text="Добавить", command=add_student_data_to_database)
add_button.grid(row=0, column=1, sticky=NE)
refresh_button = ttk.Button(main_window, text="Обновить", command=refresh_viewport_data_with_student)
refresh_button.grid(row=0, column=2, sticky=N)

main_window.mainloop()
connection.close()