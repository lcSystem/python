#!/bin/bash

echo "Instalando Python 3 y librerias necesarias..."

sudo apt update

echo "Instalando Python 3 y pip..."
sudo apt install -y python3 python3-pip

python3 --version
if [ $? -ne 0 ]; then
    echo "Error: No se pudo instalar Python."
    exit 1
fi

pip3 --version
if [ $? -ne 0 ]; then
    echo "Error: No se pudo instalar pip."
    exit 1
fi

echo "Instalando librerias necesarias..."
pip3 install tkinter

echo "Instalacion completa."

