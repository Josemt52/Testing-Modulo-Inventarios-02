import mysql.connector

def init_db(app):
    app.config['DB_HOST'] = 'localhost'
    app.config['DB_USER'] = 'root'
    app.config['DB_PASSWORD'] = '2124'
    app.config['DB_NAME'] = 'inventario_db'

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='2124',
        database='inventario_db'
    )
