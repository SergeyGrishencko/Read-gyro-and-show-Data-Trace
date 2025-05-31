import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
import gyro_read

def open_file_dialog():
    """Открывает диалог выбора файла и вставляет путь в поле ввода"""
    file_path = filedialog.askopenfilename(
        title="Выберите файл данных",
        filetypes=(("CSV files", "*.csv"), ("Все файлы", "*.*"))
    )
    if file_path:
        file_entry.delete(0, tk.END)  # Очищаем поле
        file_entry.insert(0, file_path)  # Вставляем новый путь

def plot_graphic():
    """Считывает данные из выбранного файла и строит график"""
    file_path = file_entry.get()  # Получаем путь из поля ввода
    
    if not file_path:
        status_label.config(text="Ошибка: Файл не выбран!", fg="red")
        return
    
    try:
        data = pd.read_csv(file_path)
        
        # Проверка необходимых столбцов
        required_columns = ['Time', 'Gx', 'Gy', 'Gz']
        if not all(col in data.columns for col in required_columns):
            status_label.config(text="Ошибка: Неверный формат файла", fg="red")
            return
            
        # Построение графика
        plt.figure(figsize=(10, 6))
        plt.plot(data['Time'], data['Gx'], label='X-axis')
        plt.plot(data['Time'], data['Gy'], label='Y-axis')
        plt.plot(data['Time'], data['Gz'], label='Z-axis')
        
        plt.title("Данные гироскопа")
        plt.xlabel("Время (мс)")
        plt.ylabel("Угловая скорость (°/с)")
        plt.legend()
        plt.grid(True)
        plt.show()
        
        status_label.config(text="График успешно построен!", fg="green")
        
    except Exception as e:
        status_label.config(text=f"Ошибка: {str(e)}", fg="red")

# Создание главного окна
root = tk.Tk()
root.title("Анализатор данных гироскопа")
root.geometry("600x300")

# Контейнер для элементов управления
frame = tk.Frame(root, padx=20, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

# Поле для отображения пути к файлу
file_entry = tk.Entry(frame, width=50)
file_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)

# Кнопка выбора файла
browse_btn = tk.Button(
    frame, 
    text="Выбрать файл", 
    command=open_file_dialog,
    width=15
)
browse_btn.pack(side=tk.RIGHT)

button_frame = tk.Frame(root)  # Создаем фрейм для группировки кнопок
button_frame.pack(pady=10)

# Кнопка построения графика
process_btn = tk.Button(
    button_frame,  # Помещаем кнопку в контейнер button_frame
    text="Построить график",
    width=20,
    height=2,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 10, "bold"),
    command=plot_graphic
)
process_btn.pack(side=tk.LEFT, padx=(0, 10))  # Размещаем слева с отступом справа

# Статусная метка
status_label = tk.Label(root, text="", fg="black")
status_label.pack(pady=5)

# Запуск главного цикла
root.mainloop()