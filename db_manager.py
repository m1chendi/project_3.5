from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def initialize_database():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("tree_clicker.db")

    if not db.open():
        raise Exception("Не удалось подключиться к базе данных.")

    query = QSqlQuery()
    query.exec(
        """
        CREATE TABLE IF NOT EXISTS gardener (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            salary INTEGER NOT NULL
        )
        """
    )
    return db
