from tkinter import *
from tkinter import messagebox
from tkinter import Tk, Toplevel
from tkinter.font import Font
import re
import os


DATABASE_FILE = "БД.txt"

def validate_password(password):
    pattern = r'^[a-zA-Z0-9]+$'
    return re.match(pattern, password) is not None

def is_username_available(username):
    with open(DATABASE_FILE, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "," in line:
                stored_username, _ = line.strip().split(",")
                if username == stored_username:
                    return False
    return True

def create_database_file():
    if not os.path.isfile(DATABASE_FILE):
        with open(DATABASE_FILE, "w") as file:
            pass

def register():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        if len(password) >= 8:
            if validate_password(password):
                if is_username_available(username):
                    with open(DATABASE_FILE, "a") as file:
                        file.write(f"{username},{password}\n")
                    messagebox.showinfo("Регистрация", "Регистрация успешна!")
                else:
                    messagebox.showerror("Ошибка", "Имя пользователя уже занято.")
            else:
                messagebox.showerror("Ошибка", "Пароль должен состоять только из цифр и латинских символов.")
        else:
            messagebox.showerror("Ошибка", "Пароль должен содержать минимум 8 символов.")
    else:
        messagebox.showerror("Ошибка", "Введите имя пользователя и пароль.")

def login():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        if len(password) >= 8:
            if validate_password(password):
                with open(DATABASE_FILE, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        if "," in line:
                            stored_username, stored_password = line.strip().split(",")
                            if username == stored_username and password == stored_password:
                                messagebox.showinfo("Авторизация", "Авторизация успешна!")
                                root.withdraw()  # Скрывает первое окно
                                open_empty_window()
                                return
                    messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль.")
            else:
                messagebox.showerror("Ошибка", "Пароль должен состоять только из цифр и латинских символов.")
        else:
            messagebox.showerror("Ошибка", "Пароль должен содержать минимум 8 символов.")
    else:
        messagebox.showerror("Ошибка", "Введите имя пользователя и пароль.")

show_password = False

def toggle_password_visibility():
    global show_password
    show_password = not show_password
    if show_password:
        entry_password.config(show="")
        button_show_password.config(text="Скрыть пароль")
    else:
        entry_password.config(show="*")
        button_show_password.config(text="Показать пароль")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def open_empty_window():
    empty_window = Toplevel(root)
    empty_window.title("Второе окно")
    empty_window.geometry("400x300")
    empty_window.protocol("WM_DELETE_WINDOW", lambda: [root.deiconify(), empty_window.destroy()])  # Восстанавливает первое окно и закрывает второе окно
    empty_window.mainloop()


create_database_file()

root = Tk()
root.title("Вход и регистрация")
window_width = 640
window_height = 480
center_window(root, window_width, window_height)

font = Font(family="Arial", size=12)

main_frame = Frame(root)
main_frame.pack(expand=True)
frame = Frame(main_frame)
frame.pack(pady=10,)

label_username = Label(frame, text="Имя пользователя:", font=font)
label_username.grid(row=0, column=0, pady=2, sticky="w")

label_password = Label(frame, text="Пароль:", font=font)
label_password.grid(row=1, column=0, pady=5, sticky="w")

entry_username = Entry(frame, font=font)
entry_username.grid(row=0, column=1)

entry_password = Entry(frame, show="*", font=font)
entry_password.grid(row=1, column=1)

button_show_password = Button(frame, text="Показать пароль", font=font, command=toggle_password_visibility)
button_show_password.grid(row=1, column=2, padx=5)

button_register = Button(main_frame, text="Регистрация", font=font, command=register)
button_register.pack(pady=5)

button_login = Button(main_frame, text="Войти", font=font, command=login)
button_login.pack(pady=5)

root.mainloop()