#!/bin/bash

# Ejecutar la terminal si no está ya abierta
gnome-terminal &

# Dar un pequeño tiempo para que la terminal se abra completamente
sleep 1

# Obtener el ID de la ventana de la terminal recién abierta
WINDOW_ID=$(wmctrl -lx | grep "gnome-terminal" | awk '{print $1}')

# Configurar la ventana de la terminal como "siempre en la parte superior" (flotante)
wmctrl -i -r $WINDOW_ID -b add,above

# Opcional: Si quieres que la ventana sea transparente o ajustada en tamaño
# wmctrl -i -r $WINDOW_ID -e 0,100,100,800,600  # Ajustar la posición (x,y) y tamaño (ancho, alto)
# xprop -id $WINDOW_ID -f _NET_WM_WINDOW_OPACITY 32c -set _NET_WM_WINDOW_OPACITY 0xCCCCCCCC  # Opacidad

