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

# ---------------------------------------------------------[ Функціонал програми ]---------------------------------------------------------------------


# ------------------- [ Замітки ] -------------------

#  отримуємо текст із замітки з виділеною назвою та відображаємо його в полі редагування
def show_notes():
    global key                                        # зберігати текст замітки
    key = list_widget_1.selectedItems()[0].text()     # дізнаємось на яку замітку клікнули
    list_widget_2.clear()                             # очищаємо поле із тегами
    text_editor.setText(notes[key]["text"])           # відобразили текст замітки
    list_widget_2.addItems(notes[key]["tag"])         # відобразили теги замітки

#  додаємо нову замітку 
def add_notes():
    note_name,ok = QInputDialog.getText(window,'Додати замітку',"Назва замітки")    # - Створити вікно QInputDialog з назвою note_name і зчитати текст
    if note_name and ok:
        list_widget_1.addItem(note_name)                                            # - Додає замітку до віджету (списку заміток)
        notes[note_name] = {"text":"","tag":[]}                                     # - Додає до списку notes новий обєкт - але з  пустими поки полями
    writeToFile()                                                                   # - Викликаємо фукнцію для запису в Json фалу нові замітки

#  видалити вибрану замітку 
def delete_notes():
    if list_widget_1.currentItem():          # - якщо вибрана замітка
        if key in notes:                     # - і є така замітка в словнику notes (за ключем)
            notes.pop(key)                   # - pop видаляє з словника
            
            text_editor.clear()              # - очищаємо віджети
            list_widget_2.clear()
            list_widget_1.clear()
            list_widget_1.addItems(notes)    # - оновлюємо віджет списку заміток
            writeToFile()                    # - перезаписуємо файл

#  зберегти замітку 
def save_notes():
    if list_widget_1.currentItem():                       # - якщо вибрана замітка
        key = list_widget_1.currentItem().text()          # - отримати назву вибраної замітки
        notes[key]['text'] = text_editor.toPlainText()   # - записати у словник notes з текстом з віджену
        writeToFile()                                     # - перезаписати файл

# шукати по замітці
def search_for_note():

    text_to_search = text_searcher.text()
    if search_for_text.text() == 'Шукати замітку за текстом':
        filtered_notes = {}
        for key, note_data in notes.items():
            if text_to_search in note_data['text']:
                filtered_notes[key] = note_data

        search_for_text.setText('Скинути пошук')
        list_widget_1.clear()
        list_widget_1.addItems(filtered_notes.keys())
        list_widget_2.clear()
        text_editor.clear()

    elif search_for_text.text() == 'Скинути пошук':
        search_for_text.setText('Шукати замітку за текстом')
        list_widget_1.clear()
        list_widget_1.addItems(notes.keys())
        list_widget_2.clear()
        text_editor.clear()

 
# ------------------- [ Теги ] -------------------

# додати тег до нотатки

def add_tag():
    key - list_widget_1.selectedItems()[0].text()

    if key in notes:
        tag_name, ok = QInputDialog.getText(window, "Додати текст","Назва тегу:")
        if tag_name and ok:
            notes[key]["tag"].append(tag_name)
            writeToFile()
        
        tag_searcher.clear()
        list_widget_2.addItems(notes[key]["tag"])


# видалити тег з нотатки
def delete_tag():
    if key in notes:
        current_item = list_widget_2.currentItem()
        if current_item:
            tag_name = current_item.text()
            notes[key]["tag"].remove(tag_name)
            list_widget_2.takeIthem(list_widget_2.row(current_item))
            writeToFile()


# шукати по тегу
def search_note_for_tag():
    tag = tag_searcher.text()
    if search_for_tag.text() == "Шукати замітку за тегом":
        filtered_notes = {}
        for key in notes:
            if tag in notes[key]["tag"]:
              filtered_notes[key] = notes[key]
        search_for_tag.setText("Скинути пошук")

        list_widget_1.clear()
        list_widget_1.addItem(filtered_notes)
        list_widget_2.clear()
        text_editor.clear()
    elif search_for_tag.text() == "Скинути пошук":

        search_for_tag.text() == "Шукати замітку за тегом"
        list_widget_1.clear()
        list_widget_1.addIthem(notes,key[])
        list_widget_2.clear()
        text_editor.clear()
# --------------------[ Зміна теми та експорт в txt формат ] -------------------


# ------------------[ Функція для виходу з програми та зуму ]----------------------



# ------------[ Скорочення клавіші для виходу та зуму або переміщення ] -----------------


# ---------------------------------------------------------[ Запуск програми ]---------------------------------------------------------------------
#  підключення обробки подій - функцій до кнопок

make_note.clicked.connect(add_notes)
delete_note.clicked.connect(delete_note)
save_note.clicked.connect(save_note)

add_to_note.clicked.connect(add_tag)
unpin_to_note.clicked.connect(delete_note)
search_for_note.cllicked.connect(search_for_note)
search_for_tag.cllicked.connect(search_note_for_tag)

list_widget_1.itemsClicked.connect(show_notes)

# Зчитати файл
with open("notes.json", "r") as file:
    notes = json.load(file)
list_widget_1.addItems(notes) # - відобразити зчитані замітки на віджеті

# --------------------------- Закриття програми та показ
window.show()
app.exec_()
