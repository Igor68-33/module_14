import sqlite3


def initiate_db():
    file = open('database.db', 'w')
    file.close()
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    # таблица Products
    # id - целое число, первичный ключ
    # title(название продукта) - текст (не пустой)
    # description(описание) - тест
    # price(цена) - целое число (не пусто
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL,
    pict TEXT
    )
    """)

    connection.commit()
    connection.close()


def add_product(id_, title_, description_, price_, pict_):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(f"INSERT INTO Products (title,description,price,pict) VALUES (?, ?, ?, ?)",
                   (title_, description_, price_, pict_))
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    connection.commit()
    connection.close()
    return products


if __name__ == "__main__":
    initiate_db()
    for i in range(1, 5):
        add_product(f"{i}", f"Продукт {i}", f"Описание {i}", f"{100 * i}", f"BAD_{i}.webp")