# 🏺 ArtesaMarket — Versión 0.0.3

Plataforma web de artesanías colombianas con Flask + SQLite.

---

## 🚀 Instalación y ejecución

```bash
# 1. Entrar a la carpeta
cd artesaMarket

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python app.py
```

Abre tu navegador en: **http://127.0.0.1:5000**

---

## 👤 Acceso por roles

| Rol        | Cómo acceder                                      |
|------------|---------------------------------------------------|
| Cliente    | Regístrate eligiendo "Cliente"                    |
| Artesano   | Regístrate eligiendo "Artesano"                   |
| **Admin**  | Email: `admin@artesamarket.com` / Pass: `admin123`|

---

## 🗺️ Páginas disponibles

| Ruta          | Descripción                             |
|---------------|-----------------------------------------|
| `/`           | Página principal con hero + catálogo    |
| `/catalogo`   | Catálogo completo con buscador          |
| `/artesanos`  | Directorio de artesanos                 |
| `/vender`     | Publicar productos (solo artesanos)     |
| `/login`      | Inicio de sesión                        |
| `/registro`   | Crear cuenta (cliente o artesano)       |
| `/admin`      | Panel de administración (solo admin)    |

---

## 🔑 Flujo por rol

- **Cliente**: Ve el catálogo, explora artesanos.
- **Artesano**: Al iniciar sesión va a /artesanos y puede publicar productos desde /vender.
- **Admin**: Al iniciar sesión va al panel /admin con estadísticas, gestión de usuarios y productos.
