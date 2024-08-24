#Підключаємо до бібліотеки
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import json

# ------------------ Створюємо строктуру ---------------------
notes = {                                                         
    "Ласкаво просимо" : {
        "text" : "Це найкраща додаток для заміток у світі",
        "tag" : ["добро", "інструкція"] 
    }
}
 
#Функція для запису в файл
def writeToFile():
    with open("notes_data.json", "w") as file:       #Записуємо нашу структуру - сортовано у json файлі
        json.dump(notes, file, sort_keys = True)
#____________________________________________________________________

# ------------------------- Вікно програми ---------------------------
app = QApplication([])
window  = QWidget()
main_width, main_height, = 800, 600
window.setWindowTitle("Smart_notes")
window.resize(main_width,main_height)
window.setStyleSheet('background-color:#BD93D8; font-size: 16px; color: #000000')


# ------------------------- Ел. інтерфейсу ---------------------------
text_editor = QTextEdit()             # введення тексту замітки
text_editor.setStyleSheet('background-color: #9799CA;' )
text_editor.setPlaceholderText("Введіть текст..") # текст який буде триматись

list_widget1 = QListWidget()          # список заміток
list_widget1.setStyleSheet('background-color: #B47AEA')

list_widget2 = QListWidget()          # список тегів
list_widget2.setStyleSheet('background-color:#FFEE88;')

text_searcher = QLineEdit()           # пошук по тексту
text_searcher.setPlaceholderText("Введіть текст...")
text_searcher.setStyleSheet('background-color: #FE5F55')

tag_searcher = QLineEdit()           # пошук по тегу
tag_searcher.setPlaceholderText("Введіть тег...")
tag_searcher.setStyleSheet('background-color: #FE5F55')

# ------------------------- Кпопки ---------------------------
make_note = QPushButton()
make_note.setText("Створити замітку")
make_note.setStyleSheet('background-color: #7BCDBA')

delete_note = QPushButton()
delete_note.setText("Видалити замітку")
delete_note.setStyleSheet('background-color: #7BCDBA')

save_note = QPushButton()
save_note.setText("Зберегти замітку")
save_note.setStyleSheet('background-color: #7BCDBA')

add_to_note = QPushButton()
add_to_note.setText("Додати до замітки")
add_to_note.setStyleSheet('background-color:#F56438')

unpin_to_note = QPushButton()
unpin_to_note.setText("Відкріпити від замітки")
unpin_to_note.setStyleSheet('background-color: #F56438')

search_for_tag = QPushButton()
search_for_tag.setText("Шукати замітку за тегом")
search_for_tag.setStyleSheet('background-color: #F19143')

search_for_note = QPushButton()
search_for_note.setText("Шукати замітку за текстом")
search_for_note.setStyleSheet('background-color: #F19143')

action_theme_btn = QPushButton()
action_theme_btn.setText("Змінити тему")
action_theme_btn.setStyleSheet('background-color: #E69597')

# ------------------------- Розміщення на макет ---------------------------
row1 = QHBoxLayout()
row1.addWidget(make_note)
row1.addWidget(delete_note)

row2 = QHBoxLayout()
row2.addWidget(add_to_note)
row2.addWidget(unpin_to_note)

col1 = QVBoxLayout()
col1.addWidget(text_editor)

col2 = QVBoxLayout()
col2.addWidget(QLabel("Список заміток"))
col2.addWidget(list_widget1)
col2.addLayout(row1)
col2.addWidget(save_note)
col2.addWidget(QLabel("Список тегів"))
col2.addWidget(list_widget2)
col2.addWidget(QLabel("Ввід даних"))
col2.addWidget(tag_searcher)
col2.addWidget(text_searcher)
col2.addLayout(row2)
col2.addWidget(search_for_note)
col2.addWidget(search_for_tag)
col2.addWidget(action_theme_btn)

# Злиття макетів
layout_note = QHBoxLayout()
layout_note.addLayout(col1)
layout_note.addLayout(col2)

# макет на екран
window.setLayout(layout_note)
# ------------------------- 

# ________________________Функція програми__________________
#-------------------------[ Замітки ]-----------------------
#Отримує текст замітками з виділоною назвою та відображаю його в полі редагування
def show_notes():
    global key
    key = list_widget1.selectedItems() [0].text()   # Дізнаємося на яку записку клікнули
    list_widget2.cklear()                           # Очищаєо поле з тегами
    text_editor.setText(notes[key]["text"])         # Відобразили текст з замітками
    list_widget2.addItems(notes[key]["tag"])        # Відобразили теги замітками
#Додаємо нову замітки
def add_notes():
    note_name, ok =QInputDialog.getText(window,"Додати замітку", "Назва замітки")
    if note_name and ok:
        list_widget1.addItem(note_name)
        notes[note_name] = {"text": "","tag": []}
    writeToFile()

#закріпити замітку
def deleten_notes():
    if list_widget1.currentItem():          # Якщо вибирати замітку
        if key in notes:                    # І є така замітка а словнику notes
            notes.pop(key)                  # pop видиляє з словника

            text_editor.clear()                # Очищаю віджети
            list_widget2.clear()               
            list_widget1.clear()               
            list_widget1.addItems(notes)       # Очищаємо віджети списку замітки
            writeToFile                        # Перезапусковано файл

#Зберегти в замітках
def save_notes():
    if list_widget1.currentItem():                             # Якщо вибрала замітку
        key = list_widget1.currentItem().text()                # Отримати назву вибраної  замітки
        notes(key)['text'] = text_editor.toPlainText()         # Записати у словника notes з текст
        writeToFile                                            # перезапусковано файл


#підключаємо обробку події
list_widget1.itemClicked.connect(show_notes)


#-------------------------[ Теги ]-----------------------

#Зчитати файлів
with open("notes_data.json", "r") as file: 
    notes = json.load(file)
list_widget1.addItems(notes)

window.show()
app.exec()
