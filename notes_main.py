# начни тут создавать приложение с умными заметками

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, \
    QHBoxLayout, QVBoxLayout, QFormLayout, QInputDialog

import json

'''Замітки в json'''
notes = {
    "Ласкаво просимо!": {
        "текст": "Це найкращий додаток для заміток у світі!",
        "теги": ["добро", "інструкція"]
    }
}
# with open("notes_data.json", "w",encoding="utf-8") as file:
#    json.dump(notes, file)

app = QApplication([])

note_win = QWidget()
note_win.setWindowTitle("Розумні замітки")
note_win.resize(900, 600)
# //////////////////////////////////////////

list_notes = QListWidget()
list_notes_lable = QLabel("Список заміток")

button_note_crete = QPushButton("Створити замітку")
button_note_del = QPushButton("Видалити замітку")
button_note_save = QPushButton("Зберегти замітку")

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введіть тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Додати до замітки')
button_tag_del = QPushButton('Відкріпити від замітки')
button_tag_search = QPushButton('Шукати замітки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегів')
# /////////////////////////////////////////////////
layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_lable)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(button_note_crete)
row_1.addWidget(button_note_del)

col_2.addLayout(row_1)
col_2.addWidget(button_note_save)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_1 = QHBoxLayout()
row_1.addWidget(button_tag_add)
row_1.addWidget(button_tag_del)

col_2.addLayout(row_1)
col_2.addWidget(button_tag_search)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
note_win.setLayout(layout_notes)


# --------------програмування заміток------------ #
def show_notes():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])


def add_note():
    note_name, ok = QInputDialog.getText(note_win, "Додати замітку", "Назва замітки")
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
    elif not ok:
        print("not ok")


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)
            print("save")


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, ensure_ascii=False)
            print("del")
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)


# --------------програмування тегів------------ #


# ------------ кнопки заміток------------ #
list_notes.itemClicked.connect(show_notes)
button_note_crete.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
# ------------ кнопки тегів------------ #


def save_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()

        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)

            list_tags.addItem(tag)
            field_tag.clear()
            with open("notes_data.json","w", encoding="utf-8") as file:
                json.dump(notes,file, ensure_ascii=False)
                print("add tag")


def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()

        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json","w", encoding="utf-8") as file:
                json.dump(notes,file, ensure_ascii=False)
                print("del tag")


def search_tag():

    tag = field_tag.text()
    if button_tag_search.text() == "Шукати замітки по тегу":
        notes_filter = {}
        for key in notes:
            if tag in notes[key]["теги"]:
                notes_filter[key]= notes[key]
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filter)
        button_tag_search.setText("Скинути пошук")
    else:
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
button_tag_search.setText("Шукати замітки по тегу")







with open("notes_data.json", "r", encoding="utf-8") as file:
    notes = json.load(file)
list_notes.addItems(notes)

note_win.show()
app.exec_()
