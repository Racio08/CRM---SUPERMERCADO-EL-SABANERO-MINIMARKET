# 🚀 Guía de Despliegue en Producción

Esta guía describe cómo desplegar el sistema CRM en un entorno de producción.

## ⚠️ Consideraciones de Seguridad

Antes de desplegar en producción, asegúrate de:

1. **NO usar debug mode**
   - El sistema está configurado para NO usar debug por defecto
   - Nunca ejecutes `FLASK_DEBUG=true` en producción

2. **Cambiar la SECRET_KEY**
   - Edita `app.py` y cambia `app.config['SECRET_KEY']`
   - Usa una clave aleatoria y segura

3. **Usar HTTPS**
   - Configura SSL/TLS para encriptar las comunicaciones
   - Obtén un certificado SSL (Let's Encrypt es gratis)

4. **Base de datos en producción**
   - Considera usar PostgreSQL o MySQL en lugar de SQLite
   - Configura backups automáticos

## 📦 Servidor de Producción

Para producción, NO uses el servidor de desarrollo de Flask. Usa un servidor WSGI como Gunicorn.

### Instalación de Gunicorn

```bash
pip install gunicorn
```

Actualiza `requirements.txt`:
```
Flask==3.0.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
python-dotenv==1.0.0
Werkzeug==3.0.3
requests==2.32.3
gunicorn==21.2.0
```

### Ejecutar con Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

Opciones:
- `-w 4`: 4 workers (ajustar según CPU disponibles)
- `-b 0.0.0.0:5000`: Escuchar en todas las interfaces, puerto 5000

## 🔒 Configuración con Variables de Entorno

Crea un archivo `.env` (ya está en .gitignore):

```bash
# .env
SECRET_KEY=tu-clave-super-secreta-aqui
DATABASE_URI=postgresql://user:password@localhost/crm_db
FLASK_ENV=production
```

Modifica `app.py` para usar estas variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URI', 
        'sqlite:///crm_sabanero.db'
    )
    app.config['SECRET_KEY'] = os.environ.get(
        'SECRET_KEY',
        'dev-secret-key-change-in-production'
    )
    # ... resto de la configuración
```

## 🐳 Despliegue con Docker (Opcional)

Crea un `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
```

Construir y ejecutar:

```bash
docker build -t crm-sabanero .
docker run -p 5000:5000 crm-sabanero
```

## 🌐 Nginx como Proxy Reverso

Configuración de Nginx para servir el frontend y hacer proxy al backend:

```nginx
server {
    listen 80;
    server_name tudominio.com;

    # Servir frontend
    location / {
        root /var/www/crm-sabanero;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Proxy al backend API
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 💾 Migración de Base de Datos

Si cambias de SQLite a PostgreSQL:

1. Instalar psycopg2:
```bash
pip install psycopg2-binary
```

2. Actualizar URI en `.env`:
```
DATABASE_URI=postgresql://username:password@localhost/crm_sabanero
```

3. Exportar datos de SQLite (opcional):
```bash
sqlite3 crm_sabanero.db .dump > backup.sql
```

## 📊 Monitoreo y Logs

### Configurar logs

Agrega a `app.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/crm.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('CRM startup')
```

### Monitorear el servidor

Usa herramientas como:
- **Supervisor**: Para mantener Gunicorn corriendo
- **Prometheus + Grafana**: Para métricas
- **Sentry**: Para tracking de errores

## 🔄 Backups Automáticos

Script de backup diario:

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
sqlite3 crm_sabanero.db ".backup /backups/crm_$DATE.db"

# Mantener solo últimos 30 días
find /backups -name "crm_*.db" -mtime +30 -delete
```

Agregar a crontab:
```bash
0 2 * * * /path/to/backup.sh
```

## ✅ Lista de Verificación Pre-Producción

- [ ] SECRET_KEY cambiada
- [ ] DEBUG mode desactivado
- [ ] Base de datos de producción configurada
- [ ] Backups configurados
- [ ] SSL/HTTPS habilitado
- [ ] Gunicorn o servidor WSGI instalado
- [ ] Nginx o proxy reverso configurado
- [ ] Logs configurados
- [ ] Monitoreo activo
- [ ] Pruebas de carga realizadas
- [ ] Documentación actualizada
- [ ] Plan de rollback definido

## 🆘 Soporte y Mantenimiento

### Actualizar el sistema

```bash
git pull origin main
pip install -r requirements.txt --upgrade
# Reiniciar el servidor
sudo systemctl restart crm-sabanero
```

### Troubleshooting común

**Error de conexión a la base de datos:**
- Verificar credenciales en `.env`
- Verificar que el servidor de base de datos esté corriendo

**Error 502 Bad Gateway:**
- Verificar que Gunicorn esté corriendo
- Revisar logs en `/var/log/nginx/error.log`

**Rendimiento lento:**
- Aumentar número de workers en Gunicorn
- Considerar agregar Redis para caché
- Optimizar consultas a la base de datos

## 📈 Escalabilidad

Para manejar más tráfico:

1. **Caché**: Implementar Redis para sesiones y datos frecuentes
2. **Load Balancer**: Distribuir tráfico entre múltiples servidores
3. **CDN**: Servir archivos estáticos desde CDN
4. **Database Replicas**: Configurar réplicas de solo lectura

---

**Desarrollado para SUPERMERCADO EL SABANERO MINIMARKET**
