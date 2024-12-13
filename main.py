import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont  # Для управления шрифтами в Tkinter
from PIL import Image, ImageTk
import cv2
import easyocr
import pyodbc
import re

# Подключение к базе данных
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DESKTOP-ITABFPL;'
    'DATABASE=Ahmetova;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Параметры обнаружения номеров
plateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
minArea = 500
reader = easyocr.Reader(['en', 'ru'])

# Глобальные переменные
cap = None
is_running = False
frameWidth = 1000
frameHeight = 480
recognized_plates = []
current_plate_text = ""
current_plate_image = None

# Функция проверки казахстанского номера
def is_valid_kz_plate(plate_text):
    plate_pattern = r'^\d{3}[A-Za-z]{3}\d{2}$'  # Пример паттерна для KZ номеров
    return bool(re.match(plate_pattern, plate_text))


# Функция обновления списка распознанных номеров
def update_recognized_list(plate_text):
    listbox_results.insert(tk.END, plate_text)  # Добавляем номер в интерфейс
    listbox_results.yview(tk.END)  # Прокручиваем список вниз

# Функция сохранения номера и изображения
def save_plate(plate_text, plate_image):
    image_path = f".\\IMAGES\\plate_{len(recognized_plates)}.jpg"
    cv2.imwrite(image_path, plate_image)
    cursor.execute("INSERT INTO NumberPlates (PlateNumber, ImagePath) VALUES (?, ?)", plate_text, image_path)
    conn.commit()
    # Уведомление о сохранении
    messagebox.showinfo("Сохранение", f"Номер {plate_text} сохранен в базе данных.")


# Обработка кадра

def process_frame_with_easyocr(frame):
    global current_plate_text, current_plate_image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    numberPlates = plateCascade.detectMultiScale(gray, 1.1, 4)
    for (x, y, w, h) in numberPlates:
        if w * h > minArea:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            imgRoi = frame[y:y + h, x:x + w]
            results = reader.readtext(imgRoi)
            if results:
                plate_text = ''.join(e for e in results[0][1] if e.isalnum())
                if is_valid_kz_plate(plate_text) and plate_text not in recognized_plates:
                    recognized_plates.append(plate_text)  # Сохраняем номер в список
                    save_plate(plate_text, imgRoi)  # Сохраняем номер в базу
                    update_recognized_list(plate_text)  # Добавляем в интерфейс
    return frame


# Видеопоток
def update_frame():
    global cap, is_running
    if is_running and cap:
        ret, frame = cap.read()
        if ret:
            # Уменьшаем изображение (например, до половины оригинала) перед отображением
            frame_resized = cv2.resize(frame, (frameWidth // 2, frameHeight // 2))  # Подгоняем размер кадра
            processed_frame = process_frame_with_easyocr(frame_resized)  # Обработка кадра
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

            # Преобразуем в формат, который может отобразить tkinter
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)

            # Центрируем изображение на canvas
            canvas.imgtk = imgtk  # Сохраняем ссылку на изображение, чтобы оно не исчезло
            canvas.create_image(canvas.winfo_width() // 2, canvas.winfo_height() // 2, anchor="center", image=imgtk)

        canvas.after(10, update_frame)  # Периодический вызов обновления кадра


# Обновление текста с номером
def update_recognized_label(plate_text):
    listbox_results.insert(tk.END, plate_text)  # Добавляем распознанный номер

# Открытие камеры
def start_detection():
    global cap, is_running
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
    is_running = True
    update_frame()


# Закрытие по Esc
def on_key_press(event):
    if event.keysym == "Escape":
        root.destroy()

# Интерфейс
root = tk.Tk()
root.title("License Plate Recognition")
root.state("zoomed")
root.configure(bg="#1e1e2e") 

# Настройка шрифтов
large_font = ("Helvetica", 18, "bold")
medium_font = ("Helvetica", 14)

bg_color = "#282a36"  # Фон фреймов
button_color = "#6272a4"  # Цвет кнопок
button_hover = "#7084c3"  # Цвет кнопок при наведении
text_color = "#f8f8f2"  # Цвет текста

def style_button(button):
    button.configure(
        bg=button_color,
        fg=text_color,
        font=large_font,
        activebackground=button_hover,
        activeforeground=text_color,
        relief=tk.RAISED,
        bd=2
    )
frame_image = tk.Frame(root, bg=bg_color, relief=tk.RIDGE, borderwidth=3)
frame_image.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

label_source = tk.Label(frame_image, text="Live Camera Feed", font=medium_font, bg=bg_color, fg=text_color)
label_source.pack(fill="x", padx=5, pady=5)

canvas = tk.Canvas(frame_image, bg="black", width=800, height=500)
canvas.pack(fill="both", expand=True, padx=5, pady=5)

# --- Фрейм с элементами управления ---
frame_controls = tk.Frame(root, bg=bg_color, relief=tk.RIDGE, borderwidth=3)
frame_controls.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

button_detect = tk.Button(frame_controls, text="Start Detection", command=start_detection)
style_button(button_detect)
button_detect.pack(pady=20, fill="x", padx=20)



frame_results = tk.Frame(root, bg=bg_color, relief=tk.RIDGE, borderwidth=3)
frame_results.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

label_results = tk.Label(frame_results, text="Matched License Plates", font=medium_font, bg=bg_color, fg=text_color)
label_results.pack(fill="x", padx=5, pady=5)

scrollbar = tk.Scrollbar(frame_results, orient=tk.VERTICAL)
listbox_results = tk.Listbox(
    frame_results,
    height=20,
    font=medium_font,
    bg="#44475a",
    fg=text_color,
    yscrollcommand=scrollbar.set,
    selectbackground="#6272a4"
)
scrollbar.config(command=listbox_results.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox_results.pack(fill="both", expand=True, padx=5, pady=5)


# Настройка row/column для адаптации размеров
root.grid_rowconfigure(0, weight=3)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)





# Клавиша выхода
root.bind("<Key>", on_key_press)

root.mainloop()
conn.close()
