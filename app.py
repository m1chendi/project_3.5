from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QLabel, QTableView, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from db_manager import initialize_database


class TreeClicker(QMainWindow):
    def __init__(self):
        super().__init__()

       
        self.db = initialize_database()
        self.model = QSqlTableModel()
        self.model.setTable("gardener")
        self.model.select()

        self.setWindowTitle("Tree Clicker with Database")
        self.setGeometry(100, 100, 600, 400)

   
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

       
        self.layout = QVBoxLayout(self.central_widget)

    
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.layout.addWidget(self.table_view)

 
        self.name_input = QLineEdit(self, placeholderText="Имя садовника")
        self.layout.addWidget(self.name_input)
        self.salary_input = QLineEdit(self, placeholderText="Зарплата садовника")
        self.layout.addWidget(self.salary_input)


        self.add_button = QPushButton("Добавить садовника")
        self.add_button.clicked.connect(self.add_gardener)
        self.layout.addWidget(self.add_button)

        self.update_button = QPushButton("Обновить запись")
        self.update_button.clicked.connect(self.update_gardener)
        self.layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить выбранного садовника")
        self.delete_button.clicked.connect(self.delete_gardener)
        self.layout.addWidget(self.delete_button)

    def add_gardener(self):
        """Добавление нового садовника."""
        name = self.name_input.text()
        salary = self.salary_input.text()
        if not name or not salary.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректные данные.")
            return

        query = QSqlQuery()
        query.prepare("INSERT INTO gardener (name, salary) VALUES (?, ?)")
        query.addBindValue(name)
        query.addBindValue(int(salary))
        if query.exec():
            self.model.select()
            self.name_input.clear()
            self.salary_input.clear()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить садовника.")

    def update_gardener(self):
        """Обновление выбранной записи."""
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите запись для обновления.")
            return

        name = self.name_input.text()
        salary = self.salary_input.text()
        if not name or not salary.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректные данные.")
            return

        record_id = self.model.data(self.model.index(index.row(), 0))
        query = QSqlQuery()
        query.prepare("UPDATE gardener SET name = ?, salary = ? WHERE id = ?")
        query.addBindValue(name)
        query.addBindValue(int(salary))
        query.addBindValue(record_id)
        if query.exec():
            self.model.select()
            self.name_input.clear()
            self.salary_input.clear()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось обновить запись.")

    def delete_gardener(self):
        """Удаление выбранной записи."""
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")
            return

        record_id = self.model.data(self.model.index(index.row(), 0))
        query = QSqlQuery()
        query.prepare("DELETE FROM gardener WHERE id = ?")
        query.addBindValue(record_id)
        if query.exec():
            self.model.select()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить запись.")


if __name__ == "__main__":
    app = QApplication([])
    window = TreeClicker()
    window.show()
    app.exec()
