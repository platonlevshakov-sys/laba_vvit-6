# Импортируем нужные визуальные компоненты (виджеты) из библиотеки PyQt6
from PyQt6.QtWidgets import (
    QMainWindow,      # Базовый класс для главного окна программы
    QWidget,          # Базовый контейнер для элементов интерфейса
    QVBoxLayout,      # Вертикальный компоновщик (располагает элементы сверху вниз)
    QHBoxLayout,      # Горизонтальный компоновщик (располагает элементы слева направо)
    QLabel,           # Текстовая надпись (для заголовков и счетчиков)
    QLineEdit,        # Однострочное поле для ввода текста пользователем
    QPushButton,      # Обычная нажимаемая кнопка
    QListWidget,      # Список для отображения строк/задач
    QMessageBox,      # Всплывающие диалоговые окна (предупреждения, вопросы)
    QComboBox,        # Выпадающий список (для выбора приоритета)
    QListWidgetItem   # Отдельный элемент (строка) внутри QListWidget
)

# Qt содержит системные константы (роли хранения данных, выравнивание и т.д.)
from PyQt6.QtCore import Qt

# QColor используется для раскрашивания текста элементов списка
from PyQt6.QtGui import QColor


class MainWindow(QMainWindow):
    """Класс главного окна, наследуется от стандартного QMainWindow."""

    def __init__(self):
        # Обязательно вызываем конструктор родительского класса QMainWindow
        super().__init__()

        # Задаём текст в заголовке окна
        self.setWindowTitle("Менеджер задач")

        # Задаём стартовые размеры окна (ширина 550px, высота 480px)
        self.resize(550, 480)

        # Вызываем методы настройки по принципу разделения обязанностей (Задание 12)
        self.init_ui()          # 1. Создание и расстановка всех виджетов
        self.connect_signals()  # 2. Подключение кнопок к функциям-обработчикам
        self.update_counter()   # 3. Первичный расчёт и показ счётчика задач

    def init_ui(self):
        """Метод создания интерфейса и компоновки (Layouts)."""
        # QMainWindow требует обязательный центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Создаём главный вертикальный макет (всё будет строиться сверху вниз)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # 1. Текстовая подсказка над полем ввода
        self.input_label = QLabel("Новая задача:", self)
        main_layout.addWidget(self.input_label)

        # 2. Горизонтальная панель: поле ввода + выбор приоритета + кнопка
        input_layout = QHBoxLayout()

        # Поле для ввода названия задачи
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Введите название задачи...")
        input_layout.addWidget(self.task_input)

        # Выпадающий список с выбором приоритета (Самостоятельная работа)
        self.priority_combo = QComboBox(self)
        self.priority_combo.addItems(["Обычный", "Высокий", "Низкий"])
        input_layout.addWidget(self.priority_combo)

        # Кнопка добавления задачи
        self.add_button = QPushButton("Добавить", self)
        input_layout.addWidget(self.add_button)

        # Встраиваем горизонтальную строку ввода в общий вертикальный макет
        main_layout.addLayout(input_layout)

        # 3. Большой список, где отображаются добавленные задачи
        self.task_list = QListWidget(self)
        main_layout.addWidget(self.task_list)

        # 4. Горизонтальная панель с кнопками действий над задачами
        buttons_layout = QHBoxLayout()

        # Кнопка отметки задачи как выполненной (Самостоятельная работа)
        self.toggle_done_button = QPushButton("Выполнено / Активно", self)
        buttons_layout.addWidget(self.toggle_done_button)

        # Кнопка удаления одной выбранной задачи
        self.delete_button = QPushButton("Удалить", self)
        buttons_layout.addWidget(self.delete_button)

        # Кнопка удаления только выполненных задач (Самостоятельная работа)
        self.delete_done_button = QPushButton("Удалить выполненные", self)
        buttons_layout.addWidget(self.delete_done_button)

        # Кнопка полной очистки всего списка
        self.clear_button = QPushButton("Очистить всё", self)
        buttons_layout.addWidget(self.clear_button)

        # Встраиваем панель кнопок в главный вертикальный макет
        main_layout.addLayout(buttons_layout)

        # 5. Текстовая метка в самом низу окна для отображения количества задач
        self.counter_label = QLabel(self)
        main_layout.addWidget(self.counter_label)

    def connect_signals(self):
        """Связывание событий (сигналов) с методами-обработчиками (слотами)."""
        # Клик по кнопке "Добавить" -> метод add_task
        self.add_button.clicked.connect(self.add_task)

        # Нажатие клавиши Enter внутри поля ввода -> тот же метод add_task (Задание 7)
        self.task_input.returnPressed.connect(self.add_task)

        # Клик по кнопке "Удалить" -> метод delete_task
        self.delete_button.clicked.connect(self.delete_task)

        # Клик по кнопке "Очистить всё" -> метод clear_tasks
        self.clear_button.clicked.connect(self.clear_tasks)

        # Клик по кнопке выполнения -> метод toggle_task_done
        self.toggle_done_button.clicked.connect(self.toggle_task_done)

        # Клик по кнопке очистки завершённых -> метод delete_completed_tasks
        self.delete_done_button.clicked.connect(self.delete_completed_tasks)

    # ------------------- Методы-обработчики событий -------------------

    def add_task(self):
        """Добавление новой задачи в список."""
        # Получаем текст из поля ввода и удаляем лишние пробелы по краям
        text = self.task_input.text().strip()

        # Задание 6: проверка на пустую строку или строку только из пробелов
        if not text:
            # Показываем предупреждающее модальное окно с кнопкой OK
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Введите название задачи! Поле не может быть пустым."
            )
            return  # Прерываем выполнение метода, задачу не добавляем

        # Считываем текущий выбранный приоритет из выпадающего списка
        priority = self.priority_combo.currentText()

        # Создаём объект элемента списка с текстом
        item = QListWidgetItem(f"[{priority}] {text}")

        # Если приоритет "Высокий", выделяем текст красным цветом
        if priority == "Высокий":
            item.setForeground(QColor("#d9534f"))

        # В скрытое хранилище элемента (UserRole) записываем статус: False (ещё не выполнено)
        item.setData(Qt.ItemDataRole.UserRole, False)

        # Добавляем готовый элемент в наш визуальный список QListWidget
        self.task_list.addItem(item)

        # Очищаем поле ввода, чтобы пользователю было удобно вводить следующую задачу
        self.task_input.clear()

        # Обновляем счётчик задач внизу окна
        self.update_counter()

    def delete_task(self):
        """Удаление выделенной пользователем задачи."""
        # Получаем индекс (номер строки) текущей выбранной задачи (-1 если ничего не выбрано)
        row = self.task_list.currentRow()

        # Задание 8: если пользователь ничего не выбрал и нажал "Удалить"
        if row == -1:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Сначала выберите задачу в списке для удаления!"
            )
            return

        # Задание 9: диалог с вопросом и кнопками "Да" / "Нет"
        reply = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы действительно хотите удалить выбранную задачу?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  # Кнопка по умолчанию — "Нет"
        )

        # Если пользователь подтвердил удаление нажатием "Да"
        if reply == QMessageBox.StandardButton.Yes:
            # takeItem удаляет элемент из виджета и возвращает объект
            item = self.task_list.takeItem(row)
            del item  # Окончательно освобождаем память
            self.update_counter()  # Пересчитываем счётчик

    def clear_tasks(self):
        """Полная очистка всего списка задач."""
        # Задание 10: если список уже пуст, не задаём лишних вопросов
        if self.task_list.count() == 0:
            QMessageBox.information(self, "Информация", "Список задач уже пуст!")
            return

        # Запрашиваем подтверждение очистки
        reply = QMessageBox.question(
            self,
            "Подтверждение очистки",
            "Вы уверены, что хотите удалить ВСЕ задачи?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.task_list.clear()  # Полностью очищаем QListWidget
            self.update_counter()

    def toggle_task_done(self):
        """Самостоятельная работа: переключение статуса выполнения (зачёркивание)."""
        # Получаем объект текущей выбранной строки
        item = self.task_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите задачу для отметки!")
            return

        # Инвертируем текущий статус: True меняем на False, а False на True
        is_done = not item.data(Qt.ItemDataRole.UserRole)
        # Сохраняем новый статус обратно в элемент
        item.setData(Qt.ItemDataRole.UserRole, is_done)

        # Настраиваем шрифт: если задача выполнена — делаем её зачёркнутой
        font = item.font()
        font.setStrikeOut(is_done)
        item.setFont(font)

        # Выполненные задачи красим серым цветом, активные — чёрным
        item.setForeground(QColor("gray" if is_done else "black"))

        self.update_counter()

    def delete_completed_tasks(self):
        """Самостоятельная работа: удаление только завершённых задач."""
        # Находим номера всех строк, у которых статус UserRole == True
        completed_rows = [
            i for i in range(self.task_list.count())
            if self.task_list.item(i).data(Qt.ItemDataRole.UserRole)
        ]

        if not completed_rows:
            QMessageBox.information(self, "Информация", "Нет выполненных задач для удаления.")
            return

        # Удаляем с конца списка к началу (reversed), чтобы индексы строк не сбивались
        for row in reversed(completed_rows):
            item = self.task_list.takeItem(row)
            del item

        self.update_counter()

    def update_counter(self):
        """Задание 11: пересчёт и обновление надписи со счётчиком внизу окна."""
        total = self.task_list.count()

        # Считаем, сколько задач имеют статус выполнено == True
        done = sum(
            1 for i in range(total)
            if self.task_list.item(i).data(Qt.ItemDataRole.UserRole)
        )

        # Устанавливаем обновлённый текст в QLabel
        self.counter_label.setText(f"Количество задач: {total} (выполнено: {done})")