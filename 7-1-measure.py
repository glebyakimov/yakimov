# Импорт необходимых библиотек
import RPi.GPIO as GPIO 
import matplotlib.pyplot as plt  
import time  

# Функция перевода числа в двоичный вид (массив битов)
def dectobin(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

# Функция для измерения напряжения с помощью АЦП
def adc():
    level = 0
    for i in range(bits - 1, -1, -1):
        level += 2**i  
        GPIO.output(dac, dectobin(level))  
        time.sleep(0.01) 
        comp_val  = GPIO.input(comp)  
        if (comp_val == 0):  
            level -= 2**i  
    return level

# Функция для отображения значения на светодиодах через ЦАП
def num2_dac_leds(value):
    signal = dectobin(value)  
    GPIO.output(dac, signal) 
    return signal

# Настройка пинов Raspberry Pi
dac = [26, 19, 13, 6, 5, 11, 9, 10]  
leds = [24, 25, 8, 7, 12, 16, 20, 21] 
comp = 4  
troyka = 17  
bits = len(dac)  
levels = 2 ** bits  
maxV = 3.3 

# Инициализация GPIO
GPIO.setmode(GPIO.BCM)  

# Настройка пинов на выход/вход
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.LOW) 
GPIO.setup(dac, GPIO.OUT) 
GPIO.setup(comp, GPIO.IN) 

GPIO.output(troyka, 0)  

# Списки для хранения данных измерений
data_volts = []  
data_times = []  

try:
    # Начало эксперимента
    start_time = time.time() 
    val = 0
    print("Зарядка\n")
    # Фаза зарядки конденсатора
    while(val < 115):
        val = adc()  
        print(" volts - {:3}".format(val / levels * maxV))
        num2_dac_leds(val)  
        data_volts.append(val)
        data_times.append(time.time() - start_time)  

    # Переключаем "Тройку" на разрядку
    GPIO.output(troyka, 1)
    print("Разрядка\n")
    # Фаза разрядки конденсатора
    while(val > 50):
        val = adc()  
        print(" volts - {:3}".format(val/levels * maxV))  
        num2_dac_leds(val) 
        data_volts.append(val)  
        data_times.append(time.time() - start_time) 

    end_time = time.time()  

    # Сохраняем настройки в файл
    with open("./settings.txt", "w") as file:
        file.write(str(len(data_volts) / (end_time - start_time)))  
        file.write(("\n"))
        file.write(str(maxV / 256))  
    
    # Вывод результатов эксперимента
    print("Наши вычисления\n")
    print("Общее время - ", end_time - start_time, " secs\n", 
          "средняя частота дискретизации - ", len(data_volts) / (end_time - start_time), "\n", 
          "период одного измерения - ",  (end_time - start_time)/ len(data_volts) , "\n",
          "Шаг квантации АЦП - ", maxV / 256)

finally:
    # Гарантированное выполнение, даже если возникла ошибка
    GPIO.output(dac, GPIO.LOW)  
    GPIO.output(troyka, GPIO.LOW)  
    GPIO.cleanup()  

# Подготовка данных для сохранения
data_times_str = [str(item) for item in data_times]
data_volts_str = [str(item) for item in data_volts]


# Сохранение данных измерений в файл
with open("data.txt", "w") as file:
    file.write("\n".join(data_volts_str))

# Построение графика
plt.plot(data_times, data_volts)
plt.show()