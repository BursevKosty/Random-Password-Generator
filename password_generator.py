import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import string


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.history_file = "history.json"
        self.history = self.load_history()

        # --- Элементы интерфейса ---
        # Ползунок длины пароля
        ttk.Label(root, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.length_scale = tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL)
        self.length_scale.set(12)
        self.length_scale.grid(row=0, column=1, padx=5, pady=5)

        # Чекбоксы для символов
        self.use_digits = tk.BooleanVar(value=True)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)

        ttk.Checkbutton(root, text="Цифры", variable=self.use_digits).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(root, text="Буквы", variable=self.use_letters).grid(row=1, column=1, sticky="w")
        ttk.Checkbutton(root, text="Спецсимволы", variable=self.use_special).grid(row=2, column=0, columnspan=2,
                                                                                  sticky="w")

        # Кнопка генерации и поле вывода
        self.password_entry = ttk.Entry(root, width=40)
        self.password_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(root, text="Сгенерировать", command=self.generate_password).grid(row=4, column=0, columnspan=2,
                                                                                    pady=5)

        # Таблица истории
        ttk.Label(root, text="История:").grid(row=5, column=0, columnspan=2, pady=(10, 0))
        self.tree = ttk.Treeview(root, columns=("password", "length", "options"), show='headings')
        self.tree.heading("password", text="Пароль")
        self.tree.heading("length", text="Длина")
        self.tree.heading("options", text="Параметры")
        self.tree.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        # Загрузка истории в таблицу
        self.update_history_table()

    def generate_password(self):
        length = self.length_scale.get()

        # Проверка корректности ввода (минимальная длина 4 уже задана в Scale)

        chars = ""
        if self.use_digits.get():
            chars += string.digits
        if self.use_letters.get():
            chars += string.ascii_letters
        if self.use_special.get():
            chars += string.punctuation

        if not chars:
            messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
            return

        password = ''.join(random.choices(chars, k=length))

        # Сохранение в историю
        options = []
        if self.use_digits.get(): options.append("цифры")
        if self.use_letters.get(): options.append("буквы")
        if self.use_special.get(): options.append("спецсимволы")

        entry = {
            "password": password,
            "length": length,
            "options": ", ".join(options),
            "timestamp": str(datetime.datetime.now())
        }

        self.history.insert(0, entry)  # Добавляем в начало списка
        self.save_history()

        # Обновление интерфейса
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.update_history_table()

    def load_history(self):
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history[:10], f, ensure_ascii=False, indent=4)  # Сохраняем только 10 последних

    def update_history_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.history:
            self.tree.insert("", tk.END, values=(item["password"], item["length"], item["options"]))


if __name__ == "__main__":
    import datetime  # Импортируем здесь или в начале файла

    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()