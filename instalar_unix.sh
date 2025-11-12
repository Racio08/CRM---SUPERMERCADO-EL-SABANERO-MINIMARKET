#!/bin/bash

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🛒 INSTALADOR CRM EL SABANERO MINIMARKET               ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

# [1/6] Verificar Python
echo -e "${YELLOW}[1/6] Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ ERROR: Python 3 no está instalado${NC}"
    echo ""
    echo "Por favor instala Python 3:"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  - Mac: brew install python@3.12"
    exit 1
fi
echo -e "${GREEN}✓ Python encontrado: $(python3 --version)${NC}"
echo ""

# [2/6] Crear entorno virtual
echo -e "${YELLOW}[2/6] Creando entorno virtual...${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ Entorno virtual ya existe${NC}"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ ERROR al crear entorno virtual${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Entorno virtual creado${NC}"
fi
echo ""

# [3/6] Activar entorno virtual
echo -e "${YELLOW}[3/6] Activando entorno virtual...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Entorno activado${NC}"
echo ""

# [4/6] Actualizar pip
echo -e "${YELLOW}[4/6] Actualizando pip...${NC}"
python -m pip install --upgrade pip --quiet
echo -e "${GREEN}✓ pip actualizado${NC}"
echo ""

# [5/6] Instalar dependencias
echo -e "${YELLOW}[5/6] Instalando dependencias...${NC}"
echo "   (Esto puede tardar unos minutos)"
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ ERROR al instalar dependencias${NC}"
    echo ""
    echo "Intentando instalación manual..."
    pip install django==4.2.7
fi
echo -e "${GREEN}✓ Dependencias instaladas${NC}"
echo ""

# [6/6] Configurar base de datos
echo -e "${YELLOW}[6/6] Configurando base de datos...${NC}"
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ ERROR al configurar base de datos${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Base de datos configurada${NC}"
echo ""

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "📋 Pasos siguientes:"
echo ""
echo "1. Crear administrador (opcional):"
echo "   python manage.py createsuperuser"
echo ""
echo "2. Crear datos de demostración (opcional):"
echo "   python crear_datos_demo.py"
echo ""
echo "3. Iniciar el servidor:"
echo "   ./iniciar.sh"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
