import numpy as np
import pandas as pd

# Параметры генерации данных
duration = 10      # Длительность записи в секундах
sample_rate = 100  # Частота дискретизации (Гц)
num_samples = duration * sample_rate

# Генерация временной оси (в миллисекундах)
time = np.linspace(0, duration * 1000, num_samples)

# Генерация данных для осей X, Y, Z с разными частотами
# Основные сигналы (синусоиды с разными параметрами)
gx = 2.5 * np.sin(2 * np.pi * 0.5 * time/1000)  # Низкочастотное колебание
gy = 1.8 * np.sin(2 * np.pi * 1.2 * time/1000 + 0.5)  # Средняя частота
gz = 4.0 * np.sin(2 * np.pi * 0.2 * time/1000)  # Очень низкая частота

# Добавление резких изменений (имитация движений)
gx[300:400] += 3.0 * np.sin(2 * np.pi * 5.0 * time[300:400]/1000)
gy[600:700] -= 2.5 * np.sin(2 * np.pi * 3.0 * time[600:700]/1000)
gz[800:900] += 4.0

# Добавление случайного шума
noise_intensity = 0.15
gx += noise_intensity * np.random.randn(num_samples)
gy += noise_intensity * np.random.randn(num_samples)
gz += noise_intensity * np.random.randn(num_samples)

# Создание DataFrame
data = pd.DataFrame({
    'Time': time,
    'Gx': np.round(gx, 4),
    'Gy': np.round(gy, 4),
    'Gz': np.round(gz, 4)
})

# Сохранение в CSV
data.to_csv('gyro_data.csv', index=False)
print("Файл gyro_data.csv успешно создан!")