@echo off
chcp 65001 >nul
title CRM EL SABANERO MINIMARKET

echo ╔═══════════════════════════════════════════════════════════╗
echo ║   🛒 CRM EL SABANERO MINIMARKET                          ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.

echo Iniciando servidor...
echo.

REM Activar entorno virtual
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ⚠️ Entorno virtual no encontrado. Ejecuta primero: instalar_windows.bat
    pause
    exit /b 1
)

echo ✓ Entorno virtual activado
echo.
echo 🌐 El servidor se está iniciando en: http://localhost:8000/
echo.
echo 📋 CREDENCIALES:
echo    Admin: admin / admin123
echo    URL Admin: http://localhost:8000/admin/
echo.
echo ⚠️ Para detener el servidor presiona Ctrl+C
echo ═══════════════════════════════════════════════════════════
echo.

REM Abrir navegador automáticamente (opcional)
timeout /t 3 /nobreak >nul
start http://localhost:8000/

REM Iniciar servidor Django
python manage.py runserver

pause
