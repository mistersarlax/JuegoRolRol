import random
from typing import Optional
from Logica_Juego import Item, Arma, Personaje, Melee, Mago, PersonajePorDefecto, Enemigo, GuerreroOscuro, DragonMagico, EnemigoComun, Armero, Mercader

def mostrar_inventario_mercader(mercader: Mercader) -> None:
    print("Ítems disponibles en el mercader:")
    for i, item in enumerate(mercader.inventario):
        print(f"{i + 1}. {item.nombre} (Efecto: {item.efecto}, Precio: {item.precio} monedas)")

def arma_en_armero_arsenal(personaje: Personaje,arma: Arma,armero: Armero, tipo_personaje: str):
    if arma in armero.arsenal[tipo_personaje]:
        if armero.vender_arma(arma, personaje, tipo_personaje) == True:
            armero.vender_arma(arma, personaje, tipo_personaje)
            print(f"{personaje.nombre} compró {arma.nombre} por {arma.precio} monedas.")
        else:
            print(f"{personaje.nombre} no tiene suficientes monedas para comprar {arma.nombre}.")
    else:
        print(f"{arma.nombre} no está disponible para la venta.")

def actuar(enemigo: Enemigo, personaje: 'Personaje') -> None:
    accion: str = random.choice(["atacar", "defender", "usar habilidad"])
    match accion:
        case "atacar":
            print(f"{enemigo.nombre} ataca a {personaje.nombre} y le inflige {enemigo.atacar(personaje)} puntos de daño.")
        case "defender":
            print(f"{enemigo.nombre} se defiende y reduce {enemigo.defender()} puntos de daño del próximo ataque.")
        case "usar habilidad":
            enemigo.usar_habilidad(personaje)
            print(f"{enemigo.nombre} usa una habilidad especial.")

def mostrar_estado(personaje: Personaje, enemigo: Enemigo) -> None:
    print(f"--- Estado ---")
    print(f"{personaje.nombre} - Salud: {personaje.salud}, Energía: {personaje.energia}, Arma: {personaje.arma.nombre if personaje.arma else 'Sin arma'}, Monedas: {personaje.monedas}")
    print(f"{enemigo.nombre} - Salud: {enemigo.salud}")
    print("----------------")

def mostrar_estadisticas(personaje: Personaje) -> str:
    print(f"--- Stats ---")
    print(f"{personaje.nombre} - Salud: {personaje.salud}, Energía: {personaje.energia}, Arma: {personaje.arma.nombre if personaje.arma else 'Sin arma'} {personaje.arma.daño} de daño, Monedas: {personaje.monedas}")
    print("----------------")

def elegir_arma_inicial(tipo_personaje: str, armas = {
        "Melee": [Arma("Espada", 15, "físico", 50), Arma("Hacha", 20, "físico", 75)],
        "Mago": [Arma("Libro de Fuego", 25, "mágico", 100), Arma("Libro de Hielo", 20, "mágico", 90)],
        "Defecto": [Arma("Puños", 5, "físico", 0)]
    }) -> Optional[Arma]:

    while True:
        if tipo_personaje in armas:
            print("Armas disponibles:")
            for i, arma in enumerate(armas[tipo_personaje]):
                print(f"{i + 1}. {arma.nombre} (Daño: {arma.daño}, Precio: {arma.precio})")
            eleccion = int(input("Selecciona un arma: ")) - 1
            if 0 <= eleccion < len(armas[tipo_personaje]):
                return armas[tipo_personaje][eleccion]
            else:
                print("Opción no válida, intenta de nuevo")
        else:
            print("Tipo de personaje no válido.")
            return None

def combate(personaje: Personaje, enemigo: Enemigo) -> None:
    while personaje.salud > 0 and enemigo.salud > 0:
        print(f"--- Turno de {personaje.nombre} ---")
        mostrar_estado(personaje, enemigo)

        accion = input("Elige una acción: 1. Atacar 2. Usar ítem 3. Defender: ")
        match accion:
            case "1":
                if isinstance(personaje, Melee) or isinstance(personaje, PersonajePorDefecto):
                    print(f"{personaje.nombre} ataca a {enemigo.nombre} con {personaje.arma.nombre} y le inflige {personaje.atacar(enemigo)} puntos de daño.")
                elif isinstance(personaje, Mago) and personaje.energia > 10:
                    print(f"{personaje.nombre} lanza un hechizo a {enemigo.nombre} con {personaje.arma.nombre} y le inflige {personaje.atacar(enemigo)} puntos de daño.")
                else:
                    print(f"{personaje.nombre} no tiene suficiente energía para lanzar un hechizo.")
            case "2":
                print("Ítems disponibles:")
                for i, item in enumerate(personaje.inventario):
                    print(f"{i + 1}. {item.nombre}")
                eleccion = int(input("Selecciona un ítem: ")) - 1
                if 0 <= eleccion < len(personaje.inventario):
                    personaje.usar_item(personaje.inventario[eleccion], enemigo)
                    print(f"{personaje.nombre} usó la poción de {item.efecto}")
                else:
                    print("Opción no válida.")
            case "3":
                personaje.defender()
                print(f"{personaje.nombre} se defiende y reduce el daño del próximo ataque.")
            case _:
                print("Opción no válida.")
        
        if enemigo.salud > 0:
            actuar(enemigo, personaje)
            
        if enemigo.salud <= 0:
            print(f"{enemigo.nombre} ha sido derrotado!")
            personaje.monedas += 50
            print(f"{personaje.nombre} ganó 50 monedas. Monedas actuales: {personaje.monedas}")
        if personaje.salud <= 0:
            print(f"{personaje.nombre} ha sido derrotado...")
            
def elegir_tipo_personaje():
    print("Selecciona tu personaje:")
    print("1. Guerrero (Melee)")
    print("2. Mago")
    print("3. Personaje por defecto")
    tipo_personaje = ""
    while True:
        eleccion = input("Tu elección: ")
        if eleccion == "1":
            tipo_personaje = "Melee"
            return tipo_personaje
        elif eleccion == "2":
            tipo_personaje = "Mago"
            return tipo_personaje
        elif eleccion == "3":
            tipo_personaje = "Defecto"
            return tipo_personaje
        else:
            print("Opción no válida.")
            
def crear_personaje(tipo_personaje: str, arma: Arma | None):
        if tipo_personaje == "Melee":
            personaje = Melee("Guerrero", arma)
        elif tipo_personaje == "Mago":
            personaje = Mago("Mago", arma)
        elif tipo_personaje == "Defecto":
            personaje = PersonajePorDefecto("Defensor", arma)
        return personaje
    
def mostrar_armas_armero(armero: Armero, tipo_personaje: str):
    print("Armas disponibles en el armero:")
    for i, arma in enumerate(armero.arsenal[tipo_personaje]):
        print(f"{i + 1}. {arma.nombre} (Daño: {arma.daño}, Precio: {arma.precio})")
        
def comprar_item_mercader(mercader: Mercader, personaje: Personaje):
    while True:
        eleccion_item = int(input("Selecciona un ítem para comprar: ")) - 1
        if 0 <= eleccion_item < len(mercader.inventario):
            if mercader.inventario[eleccion_item] in mercader.inventario:
                if mercader.vender_item(mercader.inventario[eleccion_item], personaje) == True:
                    mercader.vender_item(mercader.inventario[eleccion_item], personaje)
                    print(f"{personaje.nombre} compró {mercader.inventario[eleccion_item].nombre} por {mercader.inventario[eleccion_item].precio} monedas.")
                    break
                else:
                    print(f"{personaje.nombre} no tiene suficientes monedas para comprar {mercader.inventario[eleccion_item].nombre}.")
                    break
            else:
                print(f"{mercader.inventario[eleccion_item].nombre} no está disponible para la venta.")
                break
        else:
            print("Opción no válida.")
            
def elegir_arma_armero(tipo_personaje: str, armas: dict) -> Optional[Arma]:

    if tipo_personaje in armas:
        eleccion = int(input("Selecciona un arma: ")) - 1
        if 0 <= eleccion < len(armas[tipo_personaje]):
            return armas[tipo_personaje][eleccion]
        else:
            print("Opción no válida, se seleccionará un arma por defecto.")
            return armas[tipo_personaje][0]
    else:
        print("Tipo de personaje no válido.")
        return None
            
def mostrar_opciones_armero(armero: Armero, personaje: Personaje, tipo_personaje: str):
    print("Opciones del armero:")
    print("1. Comprar arma")
    print("2. Vender arma")
    print("3. Mejorar arma (Precio: 75 monedas)")
    while True:
        eleccion_armero = input("Selecciona una opción: ")
        match eleccion_armero:
            case "1":
                mostrar_armas_armero(armero, tipo_personaje)
                arma = elegir_arma_armero(tipo_personaje,armero.arsenal)
                arma_en_armero_arsenal(personaje, arma, armero, tipo_personaje)
                break
            case "2":
                if personaje.arma:
                    print(f"{personaje.nombre} vendió {personaje.arma.nombre} y recibió {personaje.arma.precio} monedas.")
                    armero.comprar_arma(personaje.arma, personaje, tipo_personaje)
                    break
                else:
                    print("No tienes ninguna arma para vender.")
                    break
            case "3":
                if personaje.arma:
                    if armero.mejorar_arma(personaje.arma, personaje) == True:
                        armero.mejorar_arma(personaje.arma, personaje)
                        print(f"{personaje.arma.nombre} mejorada en 10 puntos de daño por 75 monedas.")
                        break
                    else:
                        print(f"{personaje.nombre} no tiene suficientes monedas para mejorar {personaje.arma.nombre}.")
                        break
                else:
                    print("No tienes ninguna arma para mejorar.")
                    break
            case _:
                print("Opción no válida.")
        
def menu_principal(armero: Armero, mercader: Mercader, tipo_personaje: str, personaje: Personaje):
    while True:
            print("\nMenú Principal:")
            print("1. Ir a combate")
            print("2. Ir al armero")
            print("3. Ir al mercader")
            print("4. Mostrar estadísticas del Personaje")
            print("5. Salir del juego")
            eleccion = input("Selecciona una opción: ")
            match eleccion:
                case "1":
                    enemigo = random.choice([EnemigoComun(), DragonMagico(), GuerreroOscuro()])
                    combate(personaje, enemigo)
                case "2":
                    mostrar_opciones_armero(armero, personaje, tipo_personaje)
                case "3":
                    mostrar_inventario_mercader(mercader)
                    comprar_item_mercader(mercader, personaje)
                case "4":
                    mostrar_estadisticas(personaje)
                case "5":
                    print("Gracias por jugar. ¡Hasta la próxima!")
                    break
                case _:
                    print("Opción no válida.")