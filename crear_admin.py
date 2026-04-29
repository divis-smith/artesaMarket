import sqlite3
from werkzeug.security import generate_password_hash

def crear_usuario_admin():
    conexion = sqlite3.connect('artesaMarket.db')
    cursor = conexion.cursor()

    # Datos que quieres según tu imagen
    correo = "admin@artesamarket.com"
    nombre = "Administrador"
    # Encriptamos la contraseña "admin123"
    password_hash = generate_password_hash("admin123")
    rol = "Administrador"

    try:
        cursor.execute("INSERT INTO usuarios (nombre, correo, password, rol) VALUES (?, ?, ?, ?)",
                       (nombre, correo, password_hash, rol))
        conexion.commit()
        print("¡Usuario Administrador creado con éxito!")
    except sqlite3.IntegrityError:
        print("El administrador ya existe en la base de datos.")
    finally:
        conexion.close()

if __name__ == '__main__':
    crear_usuario_admin()