from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'clave_secreta_artesa_2026'

# ── RUTA ABSOLUTA A LA BASE DE DATOS (fix para Render) ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, 'artesaMarket.db')

def get_db():
    """Abre conexión con row_factory para acceder por nombre de columna."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea las tablas si no existen (se llama al arrancar)."""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre   TEXT NOT NULL,
            correo   TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol      TEXT NOT NULL DEFAULT 'cliente',
            region   TEXT,
            bio      TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre     TEXT NOT NULL,
            precio     REAL NOT NULL,
            emoji      TEXT DEFAULT '🏺',
            artesano_id INTEGER,
            FOREIGN KEY (artesano_id) REFERENCES usuarios(id)
        )
    ''')
    conn.commit()
    conn.close()

def crear_admin_si_no_existe():
    """Crea el usuario administrador automáticamente si no existe."""
    conn = get_db()
    existe = conn.execute(
        "SELECT id FROM usuarios WHERE correo = 'admin@artesamarket.com'"
    ).fetchone()
    if not existe:
        conn.execute(
            "INSERT INTO usuarios (nombre, correo, password, rol) VALUES (?,?,?,?)",
            ('Administrador', 'admin@artesamarket.com', generate_password_hash('admin123'), 'admin')
        )
        conn.commit()
        print("✅ Admin creado automáticamente.")
    conn.close()

# Inicializar BD y admin al arrancar (funciona en Render sin consola)
with app.app_context():
    init_db()
    crear_admin_si_no_existe()

# ── RUTAS PRINCIPALES ──

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/artesanos')
def artesanos():
    return render_template('artesanos.html')

@app.route('/vender')
def vender():
    if not session.get('user_id'):
        flash('Debes iniciar sesión para vender.', 'error')
        return redirect(url_for('login'))
    return render_template('vender.html')

# ── LOGIN ──

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        correo   = (request.form.get('correo') or '').strip().lower()
        password = request.form.get('password') or ''

        if not correo or not password:
            flash('Por favor completa todos los campos.', 'error')
            return render_template('login.html')

        conn    = get_db()
        usuario = conn.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,)).fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['password'], password):
            session.clear()
            session['user_id'] = usuario['id']
            session['nombre']  = usuario['nombre']
            session['rol']     = usuario['rol']
            flash(f'¡Bienvenido, {usuario["nombre"]}!', 'success')
            if usuario['rol'] == 'admin':
                return redirect(url_for('admin_panel'))
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos.', 'error')

    return render_template('login.html')

# ── LOGOUT ──

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'success')
    return redirect(url_for('index'))

# ── REGISTRO ──

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if session.get('user_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre   = (request.form.get('nombre') or '').strip()
        correo   = (request.form.get('correo') or '').strip().lower()
        password = request.form.get('password') or ''
        rol      = request.form.get('rol') or 'cliente'
        region   = request.form.get('region') or None
        bio      = request.form.get('bio') or None

        if not nombre or not correo or not password:
            flash('Por favor completa todos los campos obligatorios.', 'error')
            return render_template('registro.html')

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'error')
            return render_template('registro.html')

        password_hash = generate_password_hash(password)

        try:
            conn = get_db()
            conn.execute(
                'INSERT INTO usuarios (nombre, correo, password, rol, region, bio) VALUES (?,?,?,?,?,?)',
                (nombre, correo, password_hash, rol, region, bio)
            )
            conn.commit()
            # Auto-login después del registro
            usuario = conn.execute('SELECT * FROM usuarios WHERE correo = ?', (correo,)).fetchone()
            conn.close()
            session.clear()
            session['user_id'] = usuario['id']
            session['nombre']  = usuario['nombre']
            session['rol']     = usuario['rol']
            flash(f'¡Cuenta creada! Bienvenido a ArtesaMarket, {nombre}.', 'success')
            return redirect(url_for('index'))

        except sqlite3.IntegrityError:
            flash('Ese correo ya está registrado. ¿Quieres iniciar sesión?', 'error')
            return render_template('registro.html')
        except Exception as e:
            flash(f'Error inesperado: {e}', 'error')
            return render_template('registro.html')

    return render_template('registro.html')

# ── PANEL ADMIN ──

@app.route('/admin')
def admin_panel():
    if session.get('rol') != 'admin':
        flash('Acceso restringido al administrador.', 'error')
        return redirect(url_for('login'))

    conn = get_db()

    usuarios   = conn.execute("SELECT id, nombre, correo, rol, region FROM usuarios ORDER BY id DESC").fetchall()
    compradores = conn.execute("SELECT id, nombre, correo, region FROM usuarios WHERE rol='cliente' ORDER BY id DESC").fetchall()
    vendedores  = conn.execute("SELECT id, nombre, correo, region, bio FROM usuarios WHERE rol='artesano' ORDER BY id DESC").fetchall()
    productos   = conn.execute('''
        SELECT p.id, p.nombre, p.precio, p.emoji, u.nombre AS artesano
        FROM productos p
        LEFT JOIN usuarios u ON p.artesano_id = u.id
        ORDER BY p.id DESC
    ''').fetchall()

    stats = {
        'total_usuarios':  conn.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0],
        'total_artesanos': conn.execute("SELECT COUNT(*) FROM usuarios WHERE rol='artesano'").fetchone()[0],
        'total_clientes':  conn.execute("SELECT COUNT(*) FROM usuarios WHERE rol='cliente'").fetchone()[0],
        'total_productos': conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0],
    }
    conn.close()

    return render_template('admin.html',
        usuarios=usuarios,
        compradores=compradores,
        vendedores=vendedores,
        productos=productos,
        stats=stats
    )

@app.route('/admin/eliminar-usuario/<int:uid>')
def eliminar_usuario(uid):
    if session.get('rol') != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    conn.execute('DELETE FROM usuarios WHERE id = ? AND rol != "admin"', (uid,))
    conn.commit()
    conn.close()
    flash('Usuario eliminado.', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/admin/eliminar-producto/<int:pid>')
def eliminar_producto(pid):
    if session.get('rol') != 'admin':
        return redirect(url_for('login'))
    conn = get_db()
    conn.execute('DELETE FROM productos WHERE id = ?', (pid,))
    conn.commit()
    conn.close()
    flash('Producto eliminado.', 'success')
    return redirect(url_for('admin_panel'))

# ── INICIO ──

if __name__ == '__main__':
    app.run(debug=True)
