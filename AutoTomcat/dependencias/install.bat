@echo off
echo Instalando Python 3 y librerias necesarias...

REM Descargar e instalar Python 3
echo Descargando e instalando Python 3...
curl -o python-installer.exe https://www.python.org/ftp/python/3.9.9/python-3.9.9-amd64.exe
start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

REM Verificar si Python se instaló correctamente
python --version
if %errorlevel% neq 0 (
    echo Error: No se pudo instalar Python.
    exit /b 1
)

REM Instalar pip
echo Instalando pip...
python -m ensurepip --upgrade

REM Verificar si pip se instaló correctamente
pip --version
if %errorlevel% neq 0 (
    echo Error: No se pudo instalar pip.
    exit /b 1
)

REM Instalar librerías necesarias
echo Instalando librerias necesarias...
pip install tkinter

echo Instalacion completa.
pause

