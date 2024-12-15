from tkinter import *
from tkinter import ttk, filedialog
from sqlite3 import *
from tkinter.messagebox import askyesno, showinfo
from time import localtime

global database_viewport

connection = connect('CourseWorkFullDB.db')
cursor = connection.cursor()

main_window = Tk()
main_window.title("Успеваемость учащихся")
main_window.geometry("1280x450")
main_window.resizable(False, False)


viewport_columns = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")

database_viewport = ttk.Treeview(main_window, show="headings", columns=viewport_columns, height=19)

database_viewport.column("1", stretch=NO, width=40)
database_viewport.column("3", stretch=NO, width=100)
database_viewport.column("4", stretch=NO, width=100)
database_viewport.column("5", stretch=NO, width=70)
database_viewport.column("6", stretch=NO, width=70)
database_viewport.column("7", stretch=NO, width=70)
database_viewport.column("8", stretch=NO, width=70)
database_viewport.column("9", stretch=NO, width=70)
database_viewport.column("10", stretch=NO, width=70)

database_viewport.grid(row=1, columnspan=4, sticky=NW, padx=20, pady=10)

def add_current_date():
    month = localtime().tm_mon
    day = localtime().tm_mday
    cursor.execute("SELECT name FROM pragma_table_info('Grade') ORDER BY cid DESC LIMIT 1")
    if cursor.fetchall()[0][0] != "{0}.{1}".format(day, month):
        cursor.execute("ALTER TABLE Grade ADD '{0}.{1}' INTEGER".format(day, month))
        connection.commit()
    else:
        pass

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
    cursor.execute("UPDATE {0} SET {0}_photo = ? WHERE ID = {2}".format(choice_table_combobox.get(), photo, database_viewport.item(database_viewport.focus())["values"][0]), [photo])
    connection.commit()

def get_image_from_database(id):
        cursor.execute("SELECT {0}_photo FROM {0} WHERE ID = {1}".format(choice_table_combobox.get(),id))
        photo = cursor.fetchall()
        photo = photo[0][0]
        write_to_file(photo, "Photo/photo.png")

def show_image_in_canvas():
    global database_image
    try:
        current_id = database_viewport.item(database_viewport.focus())["values"][0]
        get_image_from_database(current_id)
        database_image = PhotoImage(file="Photo/photo.png")
        database_image_canvas.create_image(10, 10, anchor=NW, image=database_image)
    except:
        showinfo(title="Ошибка", message="Нет фото!")



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

def clear_colums_name():
    for columns in database_viewport['columns']:
        database_viewport.heading(columns, text='')

def refresh_viewport_data():
    cursor.execute("SELECT * FROM {0}".format(choice_table_combobox.get()))
    rows = cursor.fetchall()
    match choice_table_combobox.get():
        case "Student":
            clear_colums_name()
            database_viewport.heading("1", text="№")
            database_viewport.heading("2", text="ФИО") 
            database_viewport.heading("3", text="Дата рождения")
            database_viewport.heading("4", text="Класс, группа")
            cursor.execute("SELECT ID, Full_name, Birth_date, Study_class FROM {0}".format(choice_table_combobox.get()))
            rows = cursor.fetchall()
        case "Teacher":
            clear_colums_name()
            database_viewport.heading("1", text="№")
            database_viewport.heading("2", text="ФИО") 
            database_viewport.heading("3", text="Ученая степень")
            database_viewport.heading("4", text="Стаж")
            cursor.execute("SELECT ID, Full_name, Graduation, Work_period FROM {0}".format(choice_table_combobox.get()))
            rows = cursor.fetchall()
        case "Grade":
            clear_colums_name()
            database_viewport.heading("1", text="№")
            database_viewport.heading("2", text="ФИО") 
            database_viewport.heading("3", text="Предмет")
            database_viewport.heading("5", text=cursor.description[-6][0])
            database_viewport.heading("6", text=cursor.description[-5][0])
            database_viewport.heading("7", text=cursor.description[-4][0])
            database_viewport.heading("8", text=cursor.description[-3][0])
            database_viewport.heading("9", text=cursor.description[-2][0])
            database_viewport.heading("10", text=cursor.description[-1][0])
            cursor.execute("SELECT * FROM {0}".format(choice_table_combobox.get()))
            rows = cursor.fetchall()
        case "Subject":
            clear_colums_name()
            database_viewport.heading("1", text="№")
            database_viewport.heading("2", text="Название") 
            database_viewport.heading("3", text="Имя преподавателя")
            database_viewport.heading("4", text="Часы обучения")
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

add_current_date()

main_window.mainloop()
connection.close()