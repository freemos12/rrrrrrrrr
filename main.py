import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# --- Константы ---
FILE_HISTORY = "tasks.json"
DEFAULT_TASKS = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
]

# --- Загрузка истории ---
def load_history():
    if os.path.exists(FILE_HISTORY):
        with open(FILE_HISTORY, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# --- Сохранение истории ---
def save_history(history):
    with open(FILE_HISTORY, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- Генерация задачи ---
def generate_task():
    task = random.choice(DEFAULT_TASKS)
    history.append(task)
    save_history(history)
    update_history_list()
    task_label.config(text=task["text"])

# --- Обновление списка истории ---
def update_history_list():
    history_list.delete(0, tk.END)
    for t in history:
        history_list.insert(tk.END, f"{t['text']} ({t['type']})")

# --- Фильтрация по типу ---
def filter_tasks():
    selected_type = filter_var.get()
    history_list.delete(0, tk.END)
    for t in history:
        if selected_type == "все" or t["type"] == selected_type:
            history_list.insert(tk.END, f"{t['text']} ({t['type']})")

# --- Добавление новой задачи ---
def add_task():
    text = entry_task.get().strip()
    task_type = entry_type.get().strip().lower()
    if not text or not task_type:
        messagebox.showerror("Ошибка", "Поля не должны быть пустыми!")
        return
    if task_type not in ["учёба", "спорт", "работа"]:
        messagebox.showerror("Ошибка", "Тип задачи: учёба, спорт или работа")
        return
    DEFAULT_TASKS.append({"text": text, "type": task_type})
    entry_task.delete(0, tk.END)
    entry_type.delete(0, tk.END)

# --- Инициализация ---
root = tk.Tk()
root.title("Random Task Generator")

history = load_history()

# --- Виджеты ---
tk.Label(root, text="Сгенерированная задача:").pack(pady=5)
task_label = tk.Label(root, text="", font=("Arial", 12), width=40)
task_label.pack(pady=5)

tk.Button(root, text="Сгенерировать задачу", command=generate_task).pack(pady=10)

tk.Label(root, text="История задач:").pack(pady=5)
history_list = tk.Listbox(root, width=50, height=10)
history_list.pack(pady=5)
update_history_list()

tk.Label(root, text="Фильтр по типу:").pack(pady=5)
filter_var = tk.StringVar(value="все")
for t in ["все", "учёба", "спорт", "работа"]:
    tk.Radiobutton(root, text=t, variable=filter_var, value=t, command=filter_tasks).pack(anchor="w")

tk.Label(root, text="Добавить новую задачу:").pack(pady=10)
tk.Label(root, text="Текст задачи:").pack()
entry_task = tk.Entry(root, width=40)
entry_task.pack(pady=2)
tk.Label(root, text="Тип задачи (учёба/спорт/работа):").pack()
entry_type = tk.Entry(root, width=40)
entry_type.pack(pady=2)
tk.Button(root, text="Добавить задачу", command=add_task).pack(pady=10)

# --- Запуск ---
root.mainloop()
