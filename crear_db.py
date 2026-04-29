import sqlite3

# 1. Conectamos (esto crea el archivo si no existe)
conexion = sqlite3.connect('artesaMarket.db')

# 2. Creamos un "cursor" para ejecutar comandos SQL
cursor = conexion.cursor()

# 3. Definimos la estructura de la tabla de usuarios
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        correo TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        rol TEXT NOT NULL
    )
''')

# 4. Guardamos y cerramos
conexion.commit()
conexion.close()

print("¡Base de datos y tabla de usuarios creadas con éxito!")