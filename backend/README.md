# Turnos Pro Backend

Backend Flask para el sistema de reservas multi-negocio. Incluye autenticación JWT, modelos base y rutas iniciales.

## Configuración rápida

1. Crear un entorno virtual y activar.
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configurar variables de entorno (`.env`):
   ```env
   FLASK_APP=app:create_app
   FLASK_ENV=development
   DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/turnos_pro
   JWT_SECRET_KEY=super-secret
   ```
4. Ejecutar la aplicación:
   ```bash
   flask run --app app:create_app --debug
   ```

## Estructura

- `app/__init__.py`: factoría de aplicación y registro de blueprints.
- `app/config.py`: configuración por entorno.
- `app/models.py`: modelos SQLAlchemy.
- `app/routes/`: blueprints de la API.
- `app/extensions.py`: inicialización de extensiones (DB, JWT, migraciones).

Alembic/Flask-Migrate puede inicializarse más adelante con `flask db init`.
