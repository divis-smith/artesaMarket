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
////////////////////////////////////////////////////////////////
este es el pseudo codigo de como funciona el registro de un nuevo usuario 

ALGORITMO RegistrarNuevoUsuario

    // 1. Entrada de datos desde el formulario
    LEER nombre_usuario
    LEER correo_electronico
    LEER contraseña_plana
    LEER rol_seleccionado (cliente o artesano)

    // 2. Validación de seguridad
    SI correo_electronico o contraseña_plana están vacíos ENTONCES
        MOSTRAR "Error: Todos los campos son obligatorios"
        REGRESAR al formulario
    FIN SI

    // 3. Encriptación (Seguridad de la información)
    contraseña_encriptada = GENERAR_HASH(contraseña_plana)

    // 4. Interacción con la Base de Datos
    ABRIR CONEXIÓN con "artesaMarket.db"
    
    INTENTAR
        // Verificamos que el correo no exista ya
        BUSCAR usuario DONDE correo = correo_electronico
        
        SI usuario_existe ENTONCES
            MOSTRAR "Error: El correo ya está registrado"
        SINO
            // Insertar los datos en la tabla usuarios
            INSERTAR EN tabla usuarios (nombre, correo, password, rol)
            VALORES (nombre_usuario, correo_electronico, contraseña_encriptada, rol_seleccionado)
            
            GUARDAR CAMBIOS (COMMIT)
            MOSTRAR "¡Cuenta creada con éxito! Ahora puedes iniciar sesión"
            REDIRIGIR a la página de Login
        FIN SI
        
    ATRAPAR ERROR (Si algo falla en la DB)
        MOSTRAR "Error técnico al guardar los datos"
        CANCELAR CAMBIOS (ROLLBACK)
        
    FINALMENTE
        CERRAR CONEXIÓN con la Base de Datos
    FIN INTENTAR

FIN ALGORITMO

////////////////////////////////////////////////////

![Diagrama de Flujo de Registro](./diagrama%20de%20flujo(crear%20usuario).png)