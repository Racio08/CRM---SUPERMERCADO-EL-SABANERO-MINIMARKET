@echo off
chcp 65001 >nul
title Instalador CRM EL SABANERO MINIMARKET

echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🛒 INSTALADOR CRM EL SABANERO MINIMARKET               ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no está instalado o no está en el PATH
    echo.
    echo Por favor instala Python desde: https://www.python.org/downloads/
    echo IMPORTANTE: Marca la casilla "Add Python to PATH" durante la instalación
    pause
    exit /b 1
)
echo ✓ Python encontrado
echo.

echo [2/6] Creando entorno virtual...
if exist venv (
    echo ✓ Entorno virtual ya existe
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ ERROR al crear entorno virtual
        pause
        exit /b 1
    )
    echo ✓ Entorno virtual creado
)
echo.

echo [3/6] Activando entorno virtual...
call venv\Scripts\activate.bat
echo ✓ Entorno activado
echo.

echo [4/6] Actualizando pip...
python -m pip install --upgrade pip --quiet
echo ✓ pip actualizado
echo.

echo [5/6] Instalando dependencias...
echo    (Esto puede tardar unos minutos)
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ❌ ERROR al instalar dependencias
    echo.
    echo Intentando instalación manual...
    pip install django==4.2.7
)
echo ✓ Dependencias instaladas
echo.

echo [6/6] Configurando base de datos...
python manage.py migrate --noinput
if %errorlevel% neq 0 (
    echo ❌ ERROR al configurar base de datos
    pause
    exit /b 1
)
echo ✓ Base de datos configurada
echo.

echo ═══════════════════════════════════════════════════════════
echo.
echo 🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!
echo.
echo ═══════════════════════════════════════════════════════════
echo.
echo 📋 Pasos siguientes:
echo.
echo 1. Crear administrador (opcional):
echo    python manage.py createsuperuser
echo.
echo 2. Crear datos de demostración (opcional):
echo    python crear_datos_demo.py
echo.
echo 3. Iniciar el servidor:
echo    iniciar.bat
echo.
echo ═══════════════════════════════════════════════════════════
echo.
pause
