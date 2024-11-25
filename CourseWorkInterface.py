from tkinter import *
from tkinter import ttk, filedialog
from sqlite3 import *
from tkinter.messagebox import askyesno, showinfo

connection = connect("C:/Users/Даниил/Desktop/Курсовая работа/CourseWorkFullDB.db")
cursor = connection.cursor()

main_window = Tk()
main_window.title("Успеваемость учащихся")
main_window.geometry("1280x450")
main_window.resizable(False, False)

student_columns = ("ID", "Full_name", "Birth_date", "Study_class")

database_viewport = ttk.Treeview(main_window, show="headings", columns=student_columns, height=19)

database_viewport.heading("ID", text="№")
database_viewport.heading("Full_name", text="ФИО")
database_viewport.heading("Birth_date", text="Дата рождения")
database_viewport.heading("Study_class", text="Класс, группа")


database_viewport.grid(row=1, columnspan=4, sticky=NW, padx=20, pady=10)

def write_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def add_photo_to_chosen():
    photo_path = filedialog.askopenfile()
    photo = convert_to_binary_data(photo_path.name)
    print(choice_table_combobox.get())
    cursor.execute("UPDATE {0} SET {0}_photo = ? WHERE ID = {2}".format(choice_table_combobox.get(), photo, database_viewport.item(database_viewport.focus())["values"][0]), [photo])
    connection.commit()

def get_image_from_database(id):
        cursor.execute("SELECT {0}_photo FROM {0} WHERE ID = {1}".format(choice_table_combobox.get(),id))
        photo = cursor.fetchall()
        photo = photo[0][0]
        write_to_file(photo, "C:/Users/Даниил/Desktop/2.png")

def show_image_in_canvas():
    global database_image
    current_id = database_viewport.item(database_viewport.focus())["values"][0]
    get_image_from_database(current_id)
    database_image = PhotoImage(file="C:/Users/Даниил/Desktop/2.png")
    database_image_canvas.create_image(10, 10, anchor=NW, image=database_image)



def add_student_data_to_database():

    def add_entry_to_student_table():
        ask_if_sure = askyesno(title="Подтверждение", message="Хотите  добавить?")
        if ask_if_sure:
            one_student_data = [name_entry.get(), date_entry.get(), class_entry.get()]
            cursor.execute("""
                INSERT INTO Student
                ('Full_name', 'Birth_date', 'Study_class')   
                VALUES
                (?, ?, ?)""", one_student_data)
            connection.commit()
            showinfo("Результат", "Элемент добавлен!")
        else:
            showinfo("Результат", "Операция отменена!")

    add_window = Tk()
    add_window.title("Добавить ученика")
    add_window.geometry("500x100")
    add_window.resizable(False, False)

    name_label = ttk.Label(add_window, text="ФИО", width=30)
    name_label.grid(row=0, column=0, sticky=NW, padx=20)
    date_label = ttk.Label(add_window, text="Дата рождения")
    date_label.grid(row=0, column=1, sticky=N)
    class_label = ttk.Label(add_window, text="Класс, группа")
    class_label.grid(row=0, column=2, sticky=NE, padx=25)

    name_entry = ttk.Entry(add_window, width=30)
    name_entry.grid(row=1, column=0, padx=5)
    date_entry = ttk.Entry(add_window)
    date_entry.grid(row=1, column=1, padx=5)
    class_entry = ttk.Entry(add_window)
    class_entry.grid(row=1, column=2, padx=5)

    add_button = ttk.Button(add_window, text="Добавить", command=add_entry_to_student_table)
    add_button.grid(row=2, column=2, pady=10)

def refresh_viewport_data():
    cursor.execute("SELECT * FROM {0}".format(choice_table_combobox.get()))
    rows = cursor.fetchall()

    for i in database_viewport.get_children():
        database_viewport.delete(i)

    for row in rows:
        database_viewport.insert("", END, values=row)


tables = ["Student", "Teacher", "Subject", "Grade"]
take_table = StringVar(value=tables[3])
choice_table_combobox = ttk.Combobox(textvariable=take_table, values=tables)
choice_table_combobox.grid(row=0, column=0, sticky=W, padx=20)

add_button = ttk.Button(main_window, text="Добавить", command=add_student_data_to_database)
add_button.grid(row=0, column=1)
refresh_button = ttk.Button(main_window, text="Обновить", command=refresh_viewport_data)
refresh_button.grid(row=0, column=3)
image_button = ttk.Button(main_window, text="Показать", command=show_image_in_canvas)
image_button.grid(row=0, column=4, sticky=N)
add_photo_button = ttk.Button(main_window, text="Добавить изображение", command=add_photo_to_chosen)
add_photo_button.grid(row=0, column=2)

database_image_canvas = Canvas(main_window, bg="white", width=400, height=400)
database_image_canvas.grid(row=1, column=4, sticky=N, pady=10)


main_window.mainloop()
connection.close()