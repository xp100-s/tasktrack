import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QGridLayout, QWidget, QScrollArea
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import Qt
import json
jsonfile = 'saved.json'
add_input = ''

with open(jsonfile, 'r', encoding='utf-8') as f:
    data = json.load(f)
tasks_list = [item["task"] for item in data["tasksd"]]
status = [item["done"] for item in data["tasksd"]]
tasks_text = '\n'.join(tasks_list)

blist = []
dlist = []

app = QApplication(sys.argv)
screen = QApplication.primaryScreen()
size = screen.size()
sizex = round(size.width() / 2.5)
sizey = round(sizex / 1.778)

class MainWindow(QMainWindow):
    def __init__(self):
        global tasks_text
        global status
        global add_input
        global blist
        global dlist
        global sizex, sizey
        global jsonfile
        super().__init__()
        self.initUI()
        self.refresh_tasks()
    #rebulding the whole gui
    #vibecoded the rebuilt ui. will fix later
    def initUI(self):
        global status
        global tasks_list
        global blist

        self.setWindowTitle('tasktrack')
        self.setStyleSheet("background-color: #035063;")
        self.setFixedSize(int(sizex), int(sizey))

        # 1. Создаем центральный виджет и главный макет для QMainWindow

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QGridLayout()
        main_layout.setSpacing(15)

        # --- TITLE ---
        self.title = QLabel('tasktrack', self)
        self.title.setFont(QFont('Arial', 35))
        self.title.setStyleSheet("color: #ebebeb; font-weight: bold;")
        self.title.setAlignment(Qt.AlignVCenter)
        main_layout.addWidget(self.title, 0, 0)

        # --- INPUT BOX ---
        self.add_text_box = QLineEdit(self)
        self.add_text_box.setPlaceholderText('Add tasks here')
        self.add_text_box.setStyleSheet("""
            QLineEdit { color: #ebebeb; font-weight: bold; }
            QLineEdit::placeholder { color: #6b6a6a; }
        """)
        self.add_text_box.setFont(QFont('Arial', 25))
        self.add_text_box.setAlignment(Qt.AlignVCenter)
        self.add_text_box.returnPressed.connect(self.add)
        main_layout.addWidget(self.add_text_box, 0, 1)
        
        # --- CLEAR BUTTON ---
        self.clearbtn = QPushButton("Clear", self)
        self.clearbtn.setFont(QFont('Arial', 20))
        self.clearbtn.setStyleSheet("color: #ebebeb; font-weight: bold; background-color: #023e4f; border: 1px solid #ebebeb;")
        self.clearbtn.clicked.connect(lambda: self.clear())
        main_layout.addWidget(self.clearbtn, 0, 2)
    
        # 2. Создаем отдельную внутреннюю сетку для списка задач и кнопок
        self.tasks_container = QWidget()
        self.tasks_layout = QGridLayout(self.tasks_container)
        self.tasks_layout.setSpacing(10)
        self.tasks_layout.setAlignment(Qt.AlignTop) # Прижимает список к верхнему краю
        
        # Генерируем кнопки и текст построчно, используя ваши переменные
        for i, a in enumerate(status):
            var_name = f'self.b{i}'
            if status[i] == True:
                globals()[var_name] = QPushButton('V', self)
            elif status[i] == False:
                globals()[var_name] = QPushButton('X', self)
                
            globals()[var_name].setFont(QFont('Arial', 20))
            globals()[var_name].setFixedSize(45, 35) # Фиксированный размер кнопок вместо setGeometry
            globals()[var_name].setStyleSheet("color: #ebebeb; font-weight: bold; background-color: #023e4f; border: 1px solid #ebebeb;")
            globals()[var_name].clicked.connect(lambda checked=False, current_i=i, current_b=globals()[var_name]: self.stat(current_i, current_b))
            blist.append(globals()[var_name])
            self.tasks_layout.addWidget(globals()[var_name], i, 0)

            # Создаем QLabel для текста текущей задачи и добавляем в колонку 1
            if data["tasksd"] == []:
                self.t0 = QLabel("No tasks left!")
                self.t0.setFont(QFont('Arial', 50))
                self.t0.setStyleSheet("color: #ebebeb; font-weight: bold;")
                self.t0.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.tasks_layout.addWidget(self.t0, 0, 1)
            else:
                for index, task in enumerate(tasks_list):
                    var_name = f'self.t{index}'
                    globals()[var_name] = QLabel(task, self)
                    globals()[var_name].setFont(QFont('Arial', 20))
                    globals()[var_name].setStyleSheet("color: #ebebeb; font-weight: bold;")
                    globals()[var_name].setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.tasks_layout.addWidget(globals()[var_name], index, 1)
            
            # --- TRASH BUTTONS ON THE RIGHT ---
            d_var_name = f'self.d{i}'
            globals()[d_var_name] = QPushButton('D', self) # Или используйте иконку корзины
            globals()[d_var_name].setFont(QFont('Arial', 16))
            globals()[d_var_name].setFixedSize(55, 35) # Фиксированный размер кнопки удаления
            globals()[d_var_name].setStyleSheet("color: #ff5555; font-weight: bold; background-color: #023e4f; border: 1px solid #ff5555;")
            globals()[d_var_name].clicked.connect(lambda checked=False, current_i=i: self.delete(current_i))
            dlist.append(globals()[d_var_name])
            self.tasks_layout.addWidget(globals()[d_var_name], i, 2)

        self.tasks_layout.setColumnStretch(1, 1)

        # НАСТРОЙКА QSCROLLAREA
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollArea > QWidget > QWidget { background: transparent; }
        """)
        
        # Разрешаем контейнеру расширяться
        self.tasks_container.setMinimumSize(0, 0)
        self.tasks_container.setMaximumSize(16777215, 16777215)
        
        # Помещаем контейнер ВНУТРЬ прокрутки
        self.scrollarea.setWidget(self.tasks_container)
        
        # Добавляем в главный макет ТОЛЬКО scrollarea (строка 1, под инпутом)
        main_layout.addWidget(self.scrollarea, 1, 0, 1, 2)
        main_layout.setRowStretch(1, 1)
        
        # Устанавливаем макет один раз
        central_widget.setLayout(main_layout)
        
    def refresh_tasks(self):
        # Clear existing widgets
        while self.tasks_layout.count():
            item = self.tasks_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
        # Reload data from JSON
        with open(jsonfile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tasks_list = [item["task"] for item in data["tasksd"]]
        status = [item["done"] for item in data["tasksd"]]
        
        # Store as instance variables
        self.tasks_list = tasks_list
        self.status = status
        
        # Clear lists if they're instance variables
        self.blist = []
        self.dlist = []
        
        # Rebuild task labels
        if data["tasksd"] == []:
            self.t0 = QLabel("No tasks left!", self)
            self.t0.setFont(QFont('Arial', 50))
            self.t0.setStyleSheet("color: #ebebeb; font-weight: bold;")
            self.t0.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.tasks_layout.addWidget(self.t0, 0, 1)
        else:
            for i, task in enumerate(tasks_list):
                # Create task label as self.t<i>
                var_name = f'self.t{i}'
                task_label = QLabel(task, self)
                task_label.setFont(QFont('Arial', 20))
                task_label.setStyleSheet("color: #ebebeb; font-weight: bold;")
                task_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                setattr(self, var_name, task_label)
                self.tasks_layout.addWidget(task_label, i, 1)
                
        
        # Rebuild status buttons (your exact implementation)
        for i, a in enumerate(status):
            var_name = f'b{i}'
            if status[i] == True:
                status_btn = QPushButton('V', self)
            elif status[i] == False:
                status_btn = QPushButton('X', self)
            
            status_btn.setFont(QFont('Arial', 20))
            status_btn.setFixedSize(45, 35)
            status_btn.setStyleSheet("color: #ebebeb; font-weight: bold; background-color: #023e4f; border: 1px solid #ebebeb;")
            status_btn.clicked.connect(lambda checked=False, current_i=i, current_b=status_btn: self.stat(current_i, current_b))
            
            setattr(self, var_name, status_btn)
            self.blist.append(status_btn)
            self.tasks_layout.addWidget(status_btn, i, 0)
            
            # Delete button
            delete_btn = QPushButton('D', self)
            delete_btn.setFont(QFont('Arial', 16))
            delete_btn.setFixedSize(55, 35) # Фиксированный размер кнопки удаления
            delete_btn.setStyleSheet("color: #ebebeb; font-weight: bold;  background-color: #023e4f; border: 1px solid #ff5555;")
            delete_btn.clicked.connect(lambda checked=False, current_i=i: self.delete(current_i))
            
            setattr(self, f'd{i}', delete_btn)
            self.dlist.append(delete_btn)
            self.tasks_layout.addWidget(delete_btn, i, 2)
        
        # Update tasks_text
        self.tasks_layout.parentWidget().update()  # Update the parent widget
        self.tasks_layout.update()  # Update the layout itself
        
        
    
    # Or if the layout is directly on a widget:
    # self.tasks_widget.update()  # if you have a container widget
    
    # Force Qt to process the changes immediately
        QApplication.processEvents()
        
    def save_data(self):
        with open(jsonfile, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
    def stat(self, ind, the_b):
        data["tasksd"][ind]["done"] = not data["tasksd"][ind]["done"]
        self.save_data()
        self.refresh_tasks()
    def add(self):
        add_input = self.add_text_box.text()
        if len(add_input) > 40:
            self.add_text_box.setPlaceholderText('Make it less than 40 char')
            print('You cant have more that 40 characters')
        else:
            print(add_input)
            data["tasksd"].append({"task": add_input, "done": False})
            self.save_data()
            self.refresh_tasks()
        self.add_text_box.clear()
    def delete(self, ci):
        data["tasksd"].pop(ci)
        self.save_data()
        self.refresh_tasks()
    def clear(self):
        global data, status
        
        status = [item["done"] for item in data["tasksd"]]
        
        print(f"Before clear - data tasksd: {data['tasksd']}")
        print(f"Before clear - status: {status}")
        
        for i in range(len(status) - 1, -1, -1):
            if status[i] == True:
                data["tasksd"].pop(i)
        
        status = [item["done"] for item in data["tasksd"]]
        
        print(f"After clear - data tasksd: {data['tasksd']}")
        print(f"After clear - status: {status}")
        
        self.save_data()
        self.refresh_tasks()
                
            

    
        
def main():
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()