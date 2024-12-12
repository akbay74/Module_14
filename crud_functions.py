import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Product(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
    ''')
    connection.commit()

def fill_in_products():
    for i in range(1, 5):
        cursor.execute('INSERT INTO Product (title, description, price) VALUES (?, ?, ?)',
                       (f'Продукт {i}', f'Описание {i}', i * 100))

def get_all_products():
    cursor.execute('SELECT * FROM Product')
    data = cursor.fetchall()
    connection.commit()
    return data

def add_user(username, email, age, balance = 1000):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                   (username, email, age, balance))
    connection.commit()

def is_included(name):
    check_user = cursor.execute('SELECT username FROM Users WHERE username = ?', (name,)).fetchone()
    return bool(check_user)

if __name__ == '__main__':
    initiate_db()
    if not cursor.execute('SELECT COUNT(*) from Product').fetchone()[0]:
        fill_in_products()
    connection.close()