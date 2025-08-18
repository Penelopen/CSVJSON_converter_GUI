import os, sys, pandas
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QLabel, QFileDialog
from PyQt5.QtGui import QFont

direction = 0
loaded_filepath = ''

def file_create_cnt(extension): # Создаём пустые файлы зачем-то))
    cnt = 0
    while True:
        if cnt == 0:
            file_name = f'output{extension}'
        else:
            file_name = f'output{cnt}{extension}'

        try:
            file = open(file_name, 'x')
            return file
        except FileExistsError:
            cnt += 1
opened_csv = file_create_cnt('.csv')
opened_json = file_create_cnt('.json')


def load_file():
    global loaded_filepath

    if direction == 0:
        filter_str = 'CSV файлы (*.csv)'
    elif direction == 1:
        filter_str = 'JSON файлы (*.json)'
    loaded_filepath, _ = QFileDialog.getOpenFileName(None, 'Выбрать файл', '', filter_str)

    if loaded_filepath:
        label.setText(f'Выбран файл: {loaded_filepath.split('/')[-1]}')
    else:
        label.setText('Вы забыли выбрать файл')


def direction_choice(value):
    global direction, loaded_filepath

    if value == '      CSV ⇾ JSON':
        direction = 0
    elif value == '      JSON ⇾ CSV':
        direction = 1
    loaded_filepath = '' # Сбрасываем выбранный файл при переключении


def save_result():
    global opened_csv, opened_json

    if not loaded_filepath:
        label.setText('Вы забыли выбрать файл')
    elif direction == 0: # CSV -> JSON
        try: # Проверяем не пустой-ли файл
            data = pandas.read_csv(loaded_filepath)
            data.to_json(opened_json, orient='records')
            label.setText(f'Успешно!\nфайл {opened_json.name} сохранён')
            opened_json.close() # После записи закрываем
            opened_json = file_create_cnt('.json') # И сразу открываем новый
        except pandas.errors.EmptyDataError:
            label.setText('Выбранный файл пуст')

    elif direction == 1: # JSON -> CSV
        try: # Проверяем не пустой-ли файл
            data = pandas.read_json(loaded_filepath)
            data.to_csv(opened_csv, index=False)
            label.setText(f'Успешно!\nфайл {opened_csv.name} сохранён')
            opened_csv.close() # После записи закрываем
            opened_csv = file_create_cnt('.csv') # И сразу открываем новый
        except ValueError:
            label.setText('Выбранный файл пуст')


def on_exit():

    opened_json.close()
    opened_csv.close()
    try:
        os.remove(opened_csv.name)
        os.remove(opened_json.name)
    except:
        pass

app = QApplication(sys.argv)

# Рисуем окно
window = QWidget()
window.setWindowTitle('Конвертер файлов')
window.setGeometry(400, 200, 800, 600)

# Слой с сообщениями
label = QLabel('Созданы два пустых файла.\nПатамушта так сказано в задании', parent=window)
font = QFont('Tahoma', 10)
font.setBold(True)
label.setFont(font)
label.setStyleSheet('color: #008000;')
label.setGeometry(250, 400, 300, 100)

# Кнопонька "Загрузить файл"
button = QPushButton('Загрузить файл', window)
font = QFont('Tahoma', 16)
font.setBold(True)
button.setFont(font)
button.setGeometry(250, 150, 300, 40)
button.clicked.connect(load_file)

# Выпадающий списог
combobox = QComboBox(window)
combobox.addItem('      CSV ⇾ JSON')
combobox.addItem('      JSON ⇾ CSV')
combobox.setFont(font)
combobox.setGeometry(250, 250, 300, 40)
combobox.currentTextChanged.connect(direction_choice)

# Кнопонька "Сохранить как..."
button = QPushButton('Сохранить', window)
button.setFont(font)
button.setGeometry(250, 350, 300, 40)
button.clicked.connect(save_result)

# Не забыть закрыть файлы при выходе
app.aboutToQuit.connect(on_exit)

# Магия
window.show()
app.exec()