import sqlite3

def init_db(db_name="data.db"):
    """Создание базы данных и таблицы."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clients TEXT,
            suppliers TEXT,
            subcontractors TEXT,
            credit_orgs TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_record(db_name, clients, suppliers, subcontractors, credit_orgs):
    """Добавление записи в таблицу."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO records (clients, suppliers, subcontractors, credit_orgs) VALUES (?, ?, ?, ?)",
        (clients, suppliers, subcontractors, credit_orgs)
    )
    conn.commit()
    conn.close()

def delete_record(db_name, record_id):
    """Удаление записи по ID."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

def edit_record(db_name, record_id, clients, suppliers, subcontractors, credit_orgs):
    """Редактирование записи по ID."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE records SET clients = ?, suppliers = ?, subcontractors = ?, credit_orgs = ? WHERE id = ?",
        (clients, suppliers, subcontractors, credit_orgs, record_id)
    )
    conn.commit()
    conn.close()

def load_records(db_name):
    """Загрузка всех записей из таблицы."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    rows = cursor.fetchall()
    conn.close()
    return rows
