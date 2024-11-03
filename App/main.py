from Interfaz_de_Usuario import *
from Logica_Juego import *


if __name__ == "__main__":
    armero = Armero()
    mercader = Mercader()
    tipo_personaje = elegir_tipo_personaje()
    arma = elegir_arma_inicial(tipo_personaje)
    personaje = crear_personaje(tipo_personaje, arma)
    menu_principal(armero, mercader, tipo_personaje, personaje)
