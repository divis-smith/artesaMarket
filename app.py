from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
# PASO CLAVE: Importamos la herramienta para generar el hash de seguridad
from werkzeug.security import generate_password_hash, check_password_hash # Agregamos check_password_hash
app = Flask(__name__)
# Necesario para manejar mensajes y sesiones
app.secret_key = 'clave_secreta_artesa_2026' 

# ─── RUTAS DE NAVEGACIÓN (LAS QUE HACÍAN FALTA) ───

@app.route('/')
def index():
    """Carga la página principal (Catálogo)"""
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    """Muestra el catálogo de productos"""
    return render_template('catalogo.html')

@app.route('/artesanos')
def artesanos():
    """Muestra la sección de artesanos"""
    return render_template('artesanos.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Intentamos obtener 'email' o 'correo'. Uno de los dos debe ser.
        correo_input = request.form.get('email') or request.form.get('correo')
        password = request.form.get('password')

        # Si el correo no llegó, lanzamos un error amigable en lugar de que la app explote
        if not correo_input:
            flash("Por favor, ingresa tu correo electrónico", "error")
            return render_template('login.html')

        correo = correo_input.strip().lower()

        conexion = sqlite3.connect('artesaMarket.db')
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo = ?", (correo,))
        usuario = cursor.fetchone()
        conexion.close()

        if usuario and check_password_hash(usuario[3], password):
            session.clear()
            session['user_id'] = usuario[0]
            session['nombre'] = usuario[1]
            session['rol'] = usuario[4]
            return redirect(url_for('index'))
        else:
            flash("Correo o contraseña incorrectos", "error")
            
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.clear() # Esto es vital para que el diseño vuelva a la normalidad
    flash("Sesión cerrada", "success")
    return redirect(url_for('index'))

@app.route('/vender')
def vender():
    """Ruta para el formulario de venta"""
    return render_template('vender.html')

# ─── MÓDULO DE REGISTRO CON SEGURIDAD HASH ───

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        rol = request.form.get('rol')

        password_encriptada = generate_password_hash(password)

        conexion = None
        try:
            conexion = sqlite3.connect('artesaMarket.db', timeout=10)
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, correo, password, rol) VALUES (?, ?, ?, ?)",
                           (nombre, correo, password_encriptada, rol))
            conexion.commit()
            
            flash("¡Registro exitoso! Bienvenido.", "success") # Mensaje de éxito
            return redirect(url_for('index'))
            
        except sqlite3.IntegrityError:
            flash("Error: Este correo ya está registrado.", "danger") # El error de la imagen
            return redirect(url_for('registro')) # SE QUEDA EN REGISTRO
        except Exception as e:
            flash(f"Error inesperado: {e}", "danger")
            return redirect(url_for('registro'))
        finally:
            if conexion:
                conexion.close()

    return render_template('registro.html')

# ─── INICIO AUTOMÁTICO ───
if __name__ == '__main__':
    # Lanzamos el servidor en modo debug para ver cambios en tiempo real
    app.run(debug=True)