import random
from typing import Optional
from Excepciones import OpcionInvalidaError, PersonajeInventarioVacioError, PersonajeNoTieneItemError, PersonajeNoTieneMonedasError
from Logica_Juego import Item, Arma, Personaje, Melee, Mago, PersonajePorDefecto, Enemigo, GuerreroOscuro, DragonMagico, EnemigoComun, Armero, Mercader

def mostrar_inventario_mercader(mercader: Mercader) -> None:
    print("\nÍtems disponibles en el mercader:")
    for i, item in enumerate(mercader.inventario):
        print(f"{i + 1}. {item.nombre} (Efecto: {item.efecto}, Cantidad: {item.cantidad}, Precio: {item.precio} monedas)")
        
def mostrar_inventario_personaje(personaje: Personaje) -> None:
    if personaje.inventario:
        print("\n----Ítems disponibles-----")
        for i, item in enumerate(personaje.inventario):
            print(f"{i + 1}. {item.nombre} (Efecto: {item.efecto}, Cantidad: {item.cantidad}, Precio: {item.precio} monedas)")
    else:
        raise PersonajeInventarioVacioError()

def arma_en_armero_arsenal(personaje: Personaje,arma: Arma,armero: Armero, tipo_personaje: str):
    if arma in armero.arsenal[tipo_personaje]:
        try:
            armero.vender_arma(arma, personaje, tipo_personaje)
            print(f"{personaje.nombre} compró {arma.nombre} por {arma.precio} monedas.")
        except PersonajeNoTieneMonedasError:
            print(f"{personaje.nombre} no tiene suficientes monedas para comprar {arma.nombre}.")
    else:
        print(f"{arma.nombre} no está disponible para la venta.")

def actuar_enemigo(enemigo: Enemigo, personaje: Personaje) -> None:
    accion: str = random.choice(["atacar", "defender", "usar habilidad"])
    match accion:
        case "atacar":
            print(f"\n{enemigo.nombre} ataca a {personaje.nombre} y le inflige {enemigo.atacar(personaje)} puntos de daño.")
        case "defender":
            print(f"\n{enemigo.nombre} se defiende y reduce {enemigo.defender()} puntos de daño del próximo ataque.")
        case "usar habilidad":
            enemigo.usar_habilidad(personaje)
            print(f"\n{enemigo.nombre} usa una habilidad especial.")

def mostrar_estado_combate(personaje: Personaje, enemigo: Enemigo) -> None:
    print(f"\n--- Estado ---")
    print(f"{personaje.nombre} - Salud: {personaje.salud}, Energía: {personaje.energia}, Arma: {personaje.arma.nombre if personaje.arma else 'Sin arma'}, Monedas: {personaje.monedas}")
    print(f"{enemigo.nombre} - Salud: {enemigo.salud}")
    print("----------------\n")

def elegir_arma_inicial(tipo_personaje: str, armas = {
        "Melee": [Arma("Espada", 15, "físico", 50), Arma("Hacha", 20, "físico", 75)],
        "Mago": [Arma("Libro de Fuego", 25, "mágico", 100), Arma("Libro de Hielo", 20, "mágico", 90)],
        "Defecto": [Arma("Puños", 5, "físico", 0)]
    }) -> Optional[Arma]:

    while True:
        if tipo_personaje in armas:
            while True:
                try:
                    print("\nArmas disponibles:")
                    for i, arma in enumerate(armas[tipo_personaje]):
                        print(f"{i + 1}. {arma.nombre} (Daño: {arma.daño}, Precio: {arma.precio})")
                    while True:
                        try:
                            eleccion = int(input("Selecciona un arma: ")) - 1
                            break
                        except ValueError:
                            print(f"\nOpción no válida, debes ingresar un numero entre 1 y {len(armas[tipo_personaje])}\n")
                    if 0 <= eleccion < len(armas[tipo_personaje]):
                        return armas[tipo_personaje][eleccion]
                    else:
                        raise OpcionInvalidaError()
                except OpcionInvalidaError:
                    print(f"\nOpción no válida, debes ingresar un numero entre 1 y {len(armas[tipo_personaje])}\n")
        else:
            print("Tipo de personaje no válido.")
            return None

def combate(personaje: Personaje, enemigo: Enemigo) -> None:
    while personaje.salud > 0 and enemigo.salud > 0:
        while True:
            try:
                print(f"\n--- Turno de {personaje.nombre} ---")
                mostrar_estado_combate(personaje, enemigo)
                print("Elige una acción: \n1. Atacar \n2. Usar ítem \n3. Defender")
                while True:
                    try:
                        accion = int(input("Eleccion:"))
                        break
                    except ValueError:
                        print("\nOpción no válida, debes ingresar un numero entre 1 y 3\n")
                match accion:
                    case 1:
                        if isinstance(personaje, Melee) or isinstance(personaje, PersonajePorDefecto):
                            print(f"\n{personaje.nombre} ataca a {enemigo.nombre} con {personaje.arma.nombre} y le inflige {personaje.atacar(enemigo)} puntos de daño.")
                            break
                        elif isinstance(personaje, Mago) and personaje.energia > 10:
                            print(f"\n{personaje.nombre} lanza un hechizo a {enemigo.nombre} con {personaje.arma.nombre} y le inflige {personaje.atacar(enemigo)} puntos de daño.")
                            break
                        else:
                            print(f"\n{personaje.nombre} no tiene suficiente energía para lanzar un hechizo.")
                            break
                    case 2:
                        while True:
                            try:
                                mostrar_inventario_personaje(personaje)
                                while True:
                                    try:
                                        eleccion = int(input("Selecciona un ítem: ")) - 1
                                        break
                                    except ValueError:
                                        print(f"\nOpción no válida, debes ingresar un numero entre 1 y {len(personaje.inventario)}\n")
                                if 0 <= eleccion < len(personaje.inventario):
                                    try:
                                        print(f"\n{personaje.nombre} usó la poción de {personaje.inventario[eleccion].efecto}")
                                        personaje.usar_item(personaje.inventario[eleccion], enemigo)
                                        break
                                    except PersonajeNoTieneItemError:
                                        print(f"{personaje.nombre} no tiene {personaje.inventario[eleccion].nombre}.")
                                else:
                                    raise OpcionInvalidaError()
                            except OpcionInvalidaError:
                                print(f"\nOpción no válida, debes ingresar un numero entre 1 y {len(personaje.inventario)}\n")
                            except PersonajeInventarioVacioError:
                                print(f"El inventario de {personaje.nombre} esta vacio")
                        break
                    case 3:
                        personaje.defender()
                        print(f"\n{personaje.nombre} se defiende y reduce el daño del próximo ataque.")
                        break
                    case _:
                        raise OpcionInvalidaError()
            except OpcionInvalidaError:
                print("\nOpción no válida, debes ingresar un numero entre 1 y 3\n")
        
        if enemigo.salud > 0:
            actuar_enemigo(enemigo, personaje)
            
        if enemigo.salud <= 0:
            print(f"\n{enemigo.nombre} ha sido derrotado!")
            personaje.monedas += 50
            print(f"\n{personaje.nombre} ganó 50 monedas. Monedas actuales: {personaje.monedas}")
        if personaje.salud <= 0:
            print(f"\n{personaje.nombre} ha sido derrotado...")
            
def elegir_tipo_personaje() -> str:
    print("\nSelecciona tu personaje:")
    print("1. Guerrero (Melee)")
    print("2. Mago")
    print("3. Personaje por defecto")
    tipo_personaje = ""
    while True:
        try:
            while True:
                try:
                    eleccion = int(input("Tu elección: "))
                    break
                except ValueError:
                    print("\nOpción no válida, debes ingresar un numero entre 1 y 3\n")
            match eleccion:
                case 1:
                    tipo_personaje = "Melee"
                    return tipo_personaje
                case 2:
                    tipo_personaje = "Mago"
                    return tipo_personaje
                case 3:
                    tipo_personaje = "Defecto"
                    return tipo_personaje
                case _:
                    raise OpcionInvalidaError()
                
        except OpcionInvalidaError:
            print("\nOpción no válida, debes ingresar un numero entre 1 y 3\n")
            
                
def crear_personaje(tipo_personaje: str, arma: Arma | None) -> Personaje:
        if tipo_personaje == "Melee":
            personaje = Melee("Guerrero", arma)
        elif tipo_personaje == "Mago":
            personaje = Mago("Mago", arma)
        elif tipo_personaje == "Defecto":
            personaje = PersonajePorDefecto("Defensor", arma)
        return personaje
    
def mostrar_armas_armero(armero: Armero, tipo_personaje: str) -> None:
    print("\nArmas disponibles en el armero:")
    for i, arma in enumerate(armero.arsenal[tipo_personaje]):
        print(f"{i + 1}. {arma.nombre} (Daño: {arma.daño}, Precio: {arma.precio})")
        
def comprar_item_mercader(mercader: Mercader, personaje: Personaje) -> None:
    while True:
        try:
            while True:
                try:
                    eleccion_item = int(input("\nSelecciona un ítem para comprar: ")) - 1
                    break
                except ValueError:
                    print(f"\nOpción no válida, debes ingresar un numero entre 1 y {len(mercader.inventario)}")
            if 0 <= eleccion_item < len(mercader.inventario):
                if mercader.inventario[eleccion_item] in mercader.inventario:
                    try:
                        mercader.vender_item(mercader.inventario[eleccion_item], personaje)
                        print(f"{personaje.nombre} compró {mercader.inventario[eleccion_item].nombre} por {mercader.inventario[eleccion_item].precio} monedas.")
                        break
                    except PersonajeNoTieneMonedasError:
                        print(f"{personaje.nombre} no tiene suficientes monedas para comprar {mercader.inventario[eleccion_item].nombre}.")
                        break                                                
                else:
                    print(f"Item no está disponible para la venta.")
                    break
            else:
                raise OpcionInvalidaError()
        except OpcionInvalidaError:
            print(f"\nOpción no válida, debes ingresar un numero entre 1 y {len(mercader.inventario)}")
            
def elegir_arma_armero(tipo_personaje: str, armas: dict) -> Optional[Arma]:

    if tipo_personaje in armas:
        while True:
            try:
                while True:
                    try:
                        eleccion = int(input("Selecciona un arma: ")) - 1
                        break
                    except ValueError:
                        print(f"\nOpción no válida, debes ingresar un numero entre 1 y {len(armas[tipo_personaje])}.\n")
                if 0 <= eleccion < len(armas[tipo_personaje]):
                    return armas[tipo_personaje][eleccion]
                else:
                    raise OpcionInvalidaError()
            except OpcionInvalidaError:
                print(f"\nOpción no válida, debes ingresar un numero entre 1 y {len(armas[tipo_personaje])}.\n")
    else:
        print("Tipo de personaje no válido.")
        return None
            
def mostrar_opciones_armero(armero: Armero, personaje: Personaje, tipo_personaje: str) -> None:
    print("\nOpciones del armero:")
    print("1. Comprar arma")
    print("2. Vender arma")
    print("3. Mejorar arma (Precio: 75 monedas)")
    print("4. Volver al menú principal")
    
    while True:
        try:
            while True:
                try:
                    eleccion_armero = int(input("Selecciona una opción: "))
                    break
                except ValueError:
                    print("\nOpción no válida, debes ingresar un numero entre 1 y 3.\n")
            match eleccion_armero:
                case 1:
                    mostrar_armas_armero(armero, tipo_personaje)
                    arma = elegir_arma_armero(tipo_personaje,armero.arsenal)
                    arma_en_armero_arsenal(personaje, arma, armero, tipo_personaje)
                    break
                case 2:
                    if personaje.arma:
                        print(f"{personaje.nombre} vendió {personaje.arma.nombre} y recibió {personaje.arma.precio} monedas.")
                        armero.comprar_arma(personaje.arma, personaje, tipo_personaje)
                        break
                    else:
                        print("No tienes ninguna arma para vender.")
                        break
                case 3:
                    if personaje.arma:
                        try:
                            armero.mejorar_arma(personaje.arma, personaje)
                            print(f"{personaje.arma.nombre} mejorada en 10 puntos de daño por 75 monedas.")
                            break
                        except PersonajeNoTieneMonedasError:
                            print(f"{personaje.nombre} no tiene suficientes monedas para mejorar {personaje.arma.nombre}.")
                            break
                    else:
                        print("No tienes ninguna arma para mejorar.")
                        break
                case 4:
                    print("\nRegresando al menú principal...")
                    return
                case _:
                    raise OpcionInvalidaError()
                
        except OpcionInvalidaError:
            print("\nOpción no válida, debes ingresar un numero entre 1 y 3.\n")
            
def mostrar_opciones_mercader(mercader: Mercader, personaje: Personaje) -> None:
    print("\nOpciones del Mercader:")
    print("1. Comprar items")
    print("2. Volver al menú principal")

    while True:
        try:
            while True:
                try:
                    eleccion= int(input("Selecciona una opción: "))
                    break
                except ValueError:
                    print("\nOpción no válida, debes ingresar un numero entre 1 y 2.\n")
            match eleccion:
                case 1:
                    mostrar_inventario_mercader(mercader)
                    comprar_item_mercader(mercader, personaje)
                    break
                case 2:
                    print("\nRegresando al menú principal...")
                    return
                case _:
                    raise OpcionInvalidaError()
                
        except OpcionInvalidaError:
            print("\nOpción no válida, debes ingresar un numero entre 1 y 3.\n")
        
            
        
def menu_principal(armero: Armero, mercader: Mercader, tipo_personaje: str, personaje: Personaje) -> None:
    while True:
        print("\nMenú Principal:")
        print("1. Ir a Combate")
        print("2. Ir al Armero")
        print("3. Ir al Mercader")
        print("4. Mostrar Estadísticas del Personaje")
        print("5. Mostrar Inventario del Personaje")
        print("6. Salir del Juego")
        
        try:
            while True:
                try:
                    eleccion = int(input("Selecciona una opción: "))
                    break
                except ValueError:
                    print("\nOpción no válida, debes ingresar un número entre 1 y 6.")
            match eleccion:
                case 1:
                    enemigo = random.choice([EnemigoComun(), DragonMagico(), GuerreroOscuro()])
                    combate(personaje, enemigo)
                case 2:
                    mostrar_opciones_armero(armero, personaje, tipo_personaje)
                case 3:
                    mostrar_opciones_mercader(mercader,personaje)
                case 4:
                    print(personaje)
                case 5:
                    mostrar_inventario_personaje(personaje)
                case 6:
                    print("Gracias por jugar. ¡Hasta la próxima!")
                    break
                case _:
                    raise OpcionInvalidaError()
        
        except OpcionInvalidaError:
            print("\nOpción no válida, debes ingresar un número entre 1 y 6.")
            