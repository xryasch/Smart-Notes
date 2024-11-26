from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton, QWidget, QLabel, QTextEdit, QListWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QApplication, QInputDialog, QMessageBox)
import json

notes = {
"0 Планет" :
    {
            "Текст" : "Что если вода на Марсе это признак жизни?", "Теги" : ["Марс", "Гипотезы"]
        },
"0 Чёрных дыр" :
    {
            "Текст": "Сингулярность на горизонте событий отстутствует",
            "Теги" : ["Чёрные дыры", "Факты"]
        }
}


with open("notes.json", "r") as file:
    notes = json.load(file)

app = QApplication([])
window = QWidget()
window.setWindowTitle("Умные Заметки")
window.resize(650, 500)

field_text = QTextEdit()
list1 = QLabel("Список заметок")
list2 = QListWidget()

button1 = QPushButton("Создать заметку")
button2 = QPushButton("Удалить заметку")
button3 = QPushButton("Сохранить заметку")

tags1 = QLabel("Список тегов")
tags2 = QListWidget()

field1 = QLineEdit()

button4 = QPushButton("Прикрепить заметки")
button5 = QPushButton("Открепить заметки")
button6 = QPushButton("Искать заметки по тегу")

field1.setPlaceholderText("Введите тэг")

main_lile = QHBoxLayout()
v_line1 = QVBoxLayout()
v_line2 = QVBoxLayout()
h_line1 = QHBoxLayout()
h_line2 = QHBoxLayout()

v_line1.addWidget(field_text)

v_line2.addWidget(list1)
v_line2.addWidget(list2)

h_line1.addWidget(button1)
h_line1.addWidget(button2)

v_line2.addLayout(h_line1)

v_line2.addWidget(button3)
v_line2.addWidget(tags1)
v_line2.addWidget(tags2)
v_line2.addWidget(field1)

h_line2.addWidget(button4)
h_line2.addWidget(button5)

v_line2.addLayout(h_line2)

v_line2.addWidget(button6)

main_lile.addLayout(v_line1)
main_lile.addLayout(v_line2)


window.setLayout(main_lile)


list2.addItems(notes)

def show_note():   
    name = list2.selectedItems()[0].text()
    field_text.setPlainText(notes[name]["Текст"])
    tags2.clear()
    tags2.addItems(notes[name]["Теги"])

list2.itemClicked.connect(show_note)

def add_note():
    name_note, ok = QInputDialog.getText(window, "Добавить заметку", "Введите название заметки")
    if ok and name_note != "":
        notes[name_note] = {"Текст" : "", "Теги" : []}
        list2.addItem(name_note)


def save_note():
    if list2.selectedItems():
        name = list2.selectedItems()[0].text()
        notes[name]["Текст"] = field_text.toPlainText()
        with open("notes.json", "w") as file:
            json.dump(notes, file)
    else:
        mes = QMessageBox()
        mes.setText("Заметка не выбрана")
        mes.setWindowTitle("Ошибка")
        mes.show()
        mes.exec()


button1.clicked.connect(add_note)
button3.clicked.connect(save_note)

def del_note():
    if list2.selectedItems():
        name = list2.selectedItems()[0].text()
        del notes[name]
        with open("notes.json", "w") as file:
            json.dump(notes, file)
        field_text.clear()
        list2.clear()
        tags2.clear()
        list2.addItems(notes)
    else:  
        mes = QMessageBox()
        mes.setText("Заметка не выбрана")
        mes.setWindowTitle("Ошибка")
        mes.show()
        mes.exec()

button2.clicked.connect(del_note)

def add_tag():
    if list2.selectedItems():
        name = list2.selectedItems()[0].text()
        tag_name = field1.text()
        if tag_name != "" and tag_name not in notes[name]["Теги"]:
            notes[name]["Теги"].append(tag_name)
            with open("notes.json", "w") as file:
                json.dump(notes, file)
            tags2.addItem(tag_name)

        else:
            mes = QMessageBox()
            mes.setText("Вы не написали текст для Тега, либо он уже прикреплён")
            mes.setWindowTitle("Ошибка")
            mes.show()
            mes.exec()
    else:
        mes = QMessageBox()
        mes.setText("Заметка не выбрана")
        mes.setWindowTitle("Ошибка")
        mes.show()
        mes.exec()


button4.clicked.connect(add_tag)

def del_tag():
    if list2.selectedItems():
        name = list2.selectedItems()[0].text()

        if tags2.selectedItems():
            name_tag = tags2.selectedItems()[0].text()
            notes[name]['Теги'].remove(name_tag)
            with open("notes.json", "w") as file:
                json.dump(notes, file)
            tags2.clear()
            tags2.addItems(notes[name]["Теги"])

    else:
        mes = QMessageBox()
        mes.setText("Тег не выбран")
        mes.setWindowTitle("Ошибка")
        mes.show()
        mes.exec()
button5.clicked.connect(del_tag)

def search_tag():
    tag = field1.text()
    if button6.text() == "Искать заметки по тегу" and tag:
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["Теги"]:
                notes_filtered[note]=notes[note]
        button6.setText("Сбросить поиск")
        field1.clear()
        list2.clear()
        tags2.clear()
        list2.addItems(notes_filtered)
    elif button6.text() == "Сбросить поиск":
        field1.clear()
        list2.clear()
        tags2.clear()
        list2.addItems(notes)
        button6.setText("Искать заметки по тегу")
    else:
        pass

button6.clicked.connect(search_tag)
        
window.show()
app.exec()