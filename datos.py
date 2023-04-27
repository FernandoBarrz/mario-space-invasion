# Mario Space Invasion
# Por: Fernando Barrios


# Biblioteca que permite unir las rutas estaticas a los recursos
from os.path import abspath, dirname

RUTA_BASE= abspath(dirname(__file__))
RUTA_FUENTES = RUTA_BASE+ '/fuentes/'
RUTA_IMAGENES = RUTA_BASE+ '/imagenes/'
RUTA_MUSICA = RUTA_BASE+ '/musica/'

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (78, 255, 87)
AZUL = (80, 255, 239)
MORADO = (203, 0, 255)
ROJO = (237, 28, 36)
FUENTE = RUTA_FUENTES + 'Sigmar-Regular.ttf'
NOMBRE_IMAGENES = ['mario', 'bowser', 'enemigo_1_1', 'enemigo_1_2', 'enemigo_2_1', 'enemigo_2_2', 'enemigo_3_1', 'enemigo_3_2', 'img_moneda', 'laser', 'enemylaser']

POSICION_ENEMIGO_DEFECTO = 65
MOVER_ABAJO_ENEMIGO = 35


