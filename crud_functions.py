import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Product(
id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
''')

# for i in range(1, 5):
#     cursor.execute('INSERT INTO Product (title, description, price) VALUES (?, ?, ?)',
#                    (f'Продукт {i}', f'Описание {i}', i * 100))

def get_all_products():
    cursor.execute('SELECT * FROM Product')
    data = cursor.fetchall()
    connection.commit()
    return data

# connection.commit()
# connection.close()

# if __name__ == '__main__':
#    connection.commit()
#    connection.close()
