import sys
import pandas
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QComboBox, QLabel
from PyQt5.QtGui import QFont


def load_file():

    # CSV -> JSON
    df = pd.read_csv('input.csv')
    df.to_json('output.json', orient='records')

    # JSON -> CSV
    df = pd.read_json('input.json')
    df.to_csv('output.csv', index=False)
    click_cnt = [0] # Список для хранения лишь одного значения


def direction_choice(value):
    label.setText(f"Selected: {value}")



def save_result():
    pass


app = QApplication(sys.argv)

# Рисуем окно
window = QWidget()
window.setWindowTitle('Конвертер файлов')
window.setGeometry(400, 200, 800, 600)

# Кнопонька "Загрузить файл"
button = QPushButton('Загрузить файл', window)
font = QFont('Tahoma', 16)
font.setBold(True)
button.setFont(font)
button.setGeometry(250, 200, 300, 40)
button.clicked.connect(load_file)

# Выпадающий списог
combobox = QComboBox(window)
combobox.addItem('      CSV ⇾ JSON')
combobox.addItem('      JSON ⇾ CSV')
combobox.setFont(font)
combobox.setGeometry(250, 300, 300, 40)
label = QLabel()
combobox.currentTextChanged.connect(direction_choice)

# Кнопонька "Сохранить как..."
button = QPushButton('Сохранить как...', window)
button.setFont(font)
button.setGeometry(250, 400, 300, 40)
button.clicked.connect(save_result)

# Магия
window.show()
app.exec()