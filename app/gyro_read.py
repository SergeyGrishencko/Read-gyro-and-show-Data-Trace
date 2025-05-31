import time
import sys
import random
from datetime import datetime
import csv

# Конфигурация гироскопа (MPU6050)
DEVICE_ADDR = 0x68  # Адрес I2C
PWR_MGMT_1 = 0x6B
GYRO_CONFIG = 0x1B
GYRO_XOUT = 0x43  # Начальный адрес данных гироскопа

if sys.platform.startswith('win'):
    class MockBus:
        def write_byte_data(self, addr, reg, value):
            pass
        
        def read_i2c_block_data(self, addr, reg, length):
            return [random.randint(0, 255) for _ in range(length)]
        
        def close(self):
            pass
    bus = MockBus()
    print("Режим эмуляции: Windows")
else:
    import smbus2
    bus = smbus2.SMBus(1)
    print("Режим работы с I2C")

def setup_gyro():
    """Настройка гироскопа"""
    bus.write_byte_data(DEVICE_ADDR, PWR_MGMT_1, 0)  # Выход из спящего режима
    bus.write_byte_data(DEVICE_ADDR, GYRO_CONFIG, 0)  # Диапазон ±250 °/с

def read_gyro():
    """Чтение данных гироскопа"""
    # Чтение 6 байтов (X, Y, Z)
    data = bus.read_i2c_block_data(DEVICE_ADDR, GYRO_XOUT, 6)
    
    # Конвертация в 16-битные значения
    x = (data[0] << 8) | data[1]
    y = (data[2] << 8) | data[3]
    z = (data[4] << 8) | data[5]
    
    # Конвертация в градусы/сек (±250 °/с)
    scale = 131.0  # Для диапазона ±250 °/с (LSB/°/s)
    x = x / scale
    y = y / scale
    z = z / scale
    
    return x, y, z

def write_to_csv(data, filename='gyro_data.csv'):
    """Запись данных в CSV-файл"""
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Основной цикл
if __name__ == "__main__":
    setup_gyro()
    
    # Создание файла с заголовками
    with open('gyro_data.csv', 'w') as file:
        file.write("Time,Gx,Gy,Gz\n")
    
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            x, y, z = read_gyro()
            
            # Форматирование данных
            data_row = [timestamp, x, y, z]
            print(f"Gyro: X={x:.2f}, Y={y:.2f}, Z={z:.2f} °/s")
            
            # Запись в CSV
            write_to_csv(data_row)
            
            time.sleep(0.1)  # 10 измерений в секунду
            
    except KeyboardInterrupt:
        print("\nЗапись завершена")
        bus.close()