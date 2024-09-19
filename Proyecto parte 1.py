import random
from typing import List, Optional

class Item:
    def __init__(self, nombre: str, efecto: str, cantidad: int):
        self.nombre: str = nombre
        self.efecto: str = efecto
        self.cantidad: int = cantidad

    def usar(self, personaje: 'Personaje', enemigo: 'Enemigo' = None) -> str:
        
        if self.efecto == "curación":
            personaje.salud += self.cantidad
            print(f"{personaje.nombre} se curó {self.cantidad} puntos de salud.")
            
        elif self.efecto == "revitalizar energía":
            personaje.energia += self.cantidad
            print(f"{personaje.nombre} recuperó {self.cantidad} puntos de energía.")
            
        elif self.efecto == "envenenar enemigo" and enemigo is not None:
            enemigo.salud -= self.cantidad
            print(f"{enemigo.nombre} fue envenenado y perdió {self.cantidad} puntos de salud.")

class Arma:
    def __init__(self, nombre: str, daño: int, tipo: str, precio: int) -> None:
        self.nombre: str = nombre
        self.daño: int = daño
        self.tipo: str = tipo
        self.precio: int = precio

from typing import List, Optional, Union

class Personaje:
    def __init__(self, 
                 nombre: str, 
                 salud: int, 
                 energia: int, 
                 defensa_fisica: int, 
                 defensa_magica: int, 
                 daño_fisico: int, 
                 daño_magico: int, 
                 arma: Optional[Arma], 
                 monedas: int = 100, 
                 habilidades: Optional[List[str]] = None, 
                 inventario: Optional[List[Item]] = None) -> None:
        self.nombre: str = nombre
        self.salud: int = salud
        self.energia: int = energia
        self.defensa_fisica: int = defensa_fisica
        self.defensa_magica: int = defensa_magica
        self.daño_fisico: int = daño_fisico
        self.daño_magico: int = daño_magico  
        self.arma: Optional[Arma] = arma  # Asignación del arma
        self.monedas: int = monedas  # Todos los personajes empiezan con 100 monedas
        self.habilidades: List[str] = habilidades if habilidades is not None else []
        self.inventario: List[Item] = inventario if inventario is not None else [
            Item("Curación", "curación", 20),
            Item("Revitalizar Energía", "revitalizar energía", 20),
            Item("Veneno", "envenenar enemigo", 10)
        ]

    def atacar(self, enemigo: 'Enemigo') -> None:
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

    def defender(self) -> None:
        print(f"{self.nombre} se defiende y reduce el daño del próximo ataque.")

    def usar_item(self, item: Item, enemigo: Optional['Enemigo'] = None) -> None:
        if item in self.inventario:
            item.usar(self, enemigo)  # Pasamos el enemigo si es necesario
            self.inventario.remove(item)
        else:
            print(f"{self.nombre} no tiene {item.nombre}.")


class Melee(Personaje):
    def __init__(self, 
                 nombre: str, 
                 arma: Optional[Arma]) -> None:
        habilidades: List[str] = ["Corte Rápido"]
        super().__init__(nombre=nombre, 
                         salud=150, 
                         energia=0, 
                         defensa_fisica=20, 
                         defensa_magica=5, 
                         daño_fisico=30, 
                         daño_magico=0, 
                         arma=arma, 
                         habilidades=habilidades)

    def atacar(self, enemigo: 'Enemigo') -> None:
        evento: str = random.choice(["normal", "critico", "fallo"])
        if evento == "normal":
            daño_real: int = max(self.daño_fisico + self.arma.daño - enemigo.defensa_fisica, 0)
            enemigo.salud -= daño_real
            print(f"{self.nombre} ataca a {enemigo.nombre} con {self.arma.nombre} y le inflige {daño_real} puntos de daño.")
        elif evento == "critico":
            daño_real: int = max(2 * (self.daño_fisico + self.arma.daño) - enemigo.defensa_fisica, 0)
            enemigo.salud -= daño_real
            print(f"¡Crítico! {self.nombre} ataca a {enemigo.nombre} con {self.arma.nombre} y le inflige {daño_real} puntos de daño.")
        else:
            print(f"{self.nombre} falló el ataque.")

class Mago(Personaje):
    def __init__(self, 
                 nombre: str, 
                 arma: Optional[Arma]) -> None:
        habilidades: List[str] = ["Bola de Fuego"]
        super().__init__(nombre=nombre, 
                         salud=70, 
                         energia=100, 
                         defensa_fisica=10, 
                         defensa_magica=20, 
                         daño_fisico=5, 
                         daño_magico=50, 
                         arma=arma, 
                         habilidades=habilidades)

    def atacar(self, enemigo: 'Enemigo') -> None:
        if self.energia >= 10:
            evento: str = random.choice(["normal", "critico", "fallo"])
            if evento == "normal":
                daño_real: int = max(self.daño_magico + self.arma.daño - enemigo.defensa_magica, 0)
                enemigo.salud -= daño_real
                self.energia -= 10
                print(f"{self.nombre} lanza un hechizo a {enemigo.nombre} con {self.arma.nombre} y le inflige {daño_real} puntos de daño.")
            elif evento == "critico":
                daño_real: int = max(2 * (self.daño_magico + self.arma.daño) - enemigo.defensa_magica, 0)
                enemigo.salud -= daño_real
                self.energia -= 10
                print(f"¡Crítico! {self.nombre} lanza un hechizo a {enemigo.nombre} con {self.arma.nombre} y le inflige {daño_real} puntos de daño.")
            else:
                print(f"{self.nombre} falló el hechizo.")
        else:
            print(f"{self.nombre} no tiene suficiente energía para lanzar un hechizo.")
            
class PersonajePorDefecto(Personaje):
    def __init__(self, 
                 nombre: str, 
                 arma: Optional[Arma]) -> None:
        super().__init__(nombre=nombre, 
                         salud=100, 
                         energia=0, 
                         defensa_fisica=15, 
                         defensa_magica=10, 
                         daño_fisico=15, 
                         daño_magico=0, 
                         arma=arma)

    def atacar(self, enemigo: 'Enemigo') -> None:
        evento: str = random.choice(["normal", "critico", "fallo"])
        if evento == "normal":
            daño_real: int = max(self.daño_fisico + self.arma.daño - enemigo.defensa_fisica, 0)
            enemigo.salud -= daño_real
            print(f"{self.nombre} ataca a {enemigo.nombre} con {self.arma.nombre} y le inflige {daño_real} puntos de daño.")
        elif evento == "critico":
            daño_real: int = max(2 * (self.daño_fisico + self.arma.daño) - enemigo.defensa_fisica, 0)
            enemigo.salud -= daño_real
            print(f"¡Crítico! {self.nombre} ataca a {enemigo.nombre} con {self.arma.nombre} y le inflige {daño_real} puntos de daño.")
        else:
            print(f"{self.nombre} falló el ataque.")

class Enemigo:
    def __init__(self, 
                 nombre: str, 
                 salud: int, 
                 defensa_fisica: int, 
                 defensa_magica: int, 
                 daño_fisico: int, 
                 daño_magico: int = 0) -> None:
        self.nombre = nombre
        self.salud = salud
        self.defensa_fisica = defensa_fisica
        self.defensa_magica = defensa_magica
        self.daño_fisico = daño_fisico
        self.daño_magico = daño_magico

    def actuar(self, personaje: 'Personaje') -> None:
        accion: str = random.choice(["atacar", "defender", "usar habilidad"])
        match accion:
            case "atacar":
                self.atacar(personaje)
            case "defender":
                self.defender()
            case "usar habilidad":
                self.usar_habilidad(personaje)

    def atacar(self, personaje: 'Personaje') -> None:
        daño_real: int = max(self.daño_fisico - personaje.defensa_fisica, 0)
        personaje.salud -= daño_real
        print(f"{self.nombre} ataca a {personaje.nombre} y le inflige {daño_real} puntos de daño.")

    def defender(self) -> None:
        print(f"{self.nombre} se defiende y reduce el daño del próximo ataque.")

    def usar_habilidad(self, personaje: 'Personaje') -> None:
        print(f"{self.nombre} usa una habilidad especial.")

class GuerreroOscuro(Enemigo):
    def __init__(self) -> None:
        super().__init__(nombre="Guerrero Oscuro", 
                         salud=120, 
                         defensa_fisica=15, 
                         defensa_magica=5, 
                         daño_fisico=25)

class DragonMagico(Enemigo):
    def __init__(self) -> None:
        super().__init__(nombre="Dragón Mágico", 
                         salud=150, 
                         defensa_fisica=20, 
                         defensa_magica=15, 
                         daño_fisico=20, 
                         daño_magico=30)


class EnemigoComun(Enemigo):
    def __init__(self) -> None:
        super().__init__(nombre="Esqueleto", 
                         salud=50, 
                         defensa_fisica=5, 
                         defensa_magica=5, 
                         daño_fisico=10)


class Armero:
    def __init__(self) -> None:
        self.arsenal: List[Arma] = []  # Inventario de armas disponibles para la venta

    def agregar_arma(self, arma: Arma) -> None:
        self.arsenal.append(arma)

    def vender_arma(self, arma: Arma, personaje: Personaje) -> None:
        if arma in self.arsenal:
            if personaje.monedas >= arma.precio:
                personaje.monedas -= arma.precio
                personaje.arma = arma
                self.arsenal.remove(arma)
                print(f"{personaje.nombre} compró {arma.nombre} por {arma.precio} monedas.")
            else:
                print(f"{personaje.nombre} no tiene suficientes monedas para comprar {arma.nombre}.")
        else:
            print(f"{arma.nombre} no está disponible para la venta.")

    def comprar_arma(self, arma: Arma, personaje: Personaje) -> None:
        if personaje.arma == arma:
            personaje.monedas += arma.precio
            self.arsenal.append(arma)
            personaje.arma = None  # El personaje ya no tiene el arma
            print(f"{personaje.nombre} vendió {arma.nombre} y recibió {arma.precio} monedas.")
        else:
            print(f"{personaje.nombre} no tiene el arma {arma.nombre} para vender.")

    def mejorar_arma(self, arma: Arma, personaje: Personaje, incremento: int, costo: int) -> None:
        if personaje.arma == arma:
            if personaje.monedas >= costo:
                arma.daño += incremento
                personaje.monedas -= costo
                print(f"{arma.nombre} mejorada en {incremento} puntos de daño por {costo} monedas.")
            else:
                print(f"{personaje.nombre} no tiene suficientes monedas para mejorar {arma.nombre}.")
        else:
            print(f"{personaje.nombre} no tiene el arma {arma.nombre} para mejorar.")
            
class Mercader:
    def __init__(self) -> None:
        self.inventario: List[Item] = [
            Item("Curación", "curación", 20),
            Item("Revitalizar Energía", "revitalizar energía", 20),
            Item("Veneno", "envenenar enemigo", 10)
        ]

    def mostrar_inventario(self) -> None:
        print("Ítems disponibles en el mercader:")
        for i, item in enumerate(self.inventario):
            print(f"{i + 1}. {item.nombre} (Efecto: {item.efecto}, Precio: {item.cantidad} monedas)")

    def vender_item(self, item: Item, personaje: Personaje) -> None:
        if item in self.inventario:
            if personaje.monedas >= item.cantidad:
                personaje.monedas -= item.cantidad
                personaje.inventario.append(item)
                print(f"{personaje.nombre} compró {item.nombre} por {item.cantidad} monedas.")
            else:
                print(f"{personaje.nombre} no tiene suficientes monedas para comprar {item.nombre}.")
        else:
            print(f"{item.nombre} no está disponible para la venta.")

def mostrar_estado(personaje: Personaje, enemigo: Enemigo) -> None:
    print(f"--- Estado ---")
    print(f"{personaje.nombre} - Salud: {personaje.salud}, Energía: {personaje.energia}, Arma: {personaje.arma.nombre if personaje.arma else 'Sin arma'}, Monedas: {personaje.monedas}")
    print(f"{enemigo.nombre} - Salud: {enemigo.salud}")
    print("----------------")
    
def elegir_arma(tipo_personaje: str) -> Optional[Arma]:
    armas = {
        "Melee": [Arma("Espada", 15, "físico", 50), Arma("Hacha", 20, "físico", 75)],
        "Mago": [Arma("Libro de Fuego", 25, "mágico", 100), Arma("Libro de Hielo", 20, "mágico", 90)],
        "Defecto": [Arma("Puños", 5, "físico", 0)]
    }

    if tipo_personaje in armas:
        print("Armas disponibles:")
        for i, arma in enumerate(armas[tipo_personaje]):
            print(f"{i + 1}. {arma.nombre} (Daño: {arma.daño}, Precio: {arma.precio})")
        eleccion = int(input("Selecciona un arma: ")) - 1
        if 0 <= eleccion < len(armas[tipo_personaje]):
            return armas[tipo_personaje][eleccion]
        else:
            print("Opción no válida, se seleccionará un arma por defecto.")
            return armas[tipo_personaje][0]  # Selecciona un arma por defecto
    else:
        print("Tipo de personaje no válido.")
        return None

def combate(personaje: Personaje, enemigo: Enemigo) -> None:
    while personaje.salud > 0 and enemigo.salud > 0:
        print(f"--- Turno de {personaje.nombre} ---")
        mostrar_estado(personaje, enemigo)  # Mostrar el estado antes de la acción

        accion = input("Elige una acción: 1. Atacar 2. Usar ítem 3. Defender: ")
        match accion:
            case "1":
                personaje.atacar(enemigo)
            case "2":
                print("Ítems disponibles:")
                for i, item in enumerate(personaje.inventario):
                    print(f"{i + 1}. {item.nombre}")
                eleccion = int(input("Selecciona un ítem: ")) - 1
                if 0 <= eleccion < len(personaje.inventario):
                    personaje.usar_item(personaje.inventario[eleccion], enemigo)
                else:
                    print("Opción no válida.")
            case "3":
                personaje.defender()
            case _:
                print("Opción no válida.")
        
        if enemigo.salud > 0:
            enemigo.actuar(personaje)

        if enemigo.salud <= 0:
            print(f"{enemigo.nombre} ha sido derrotado!")
            personaje.monedas += 50  # Ganar monedas al vencer al enemigo
            print(f"{personaje.nombre} ganó 50 monedas. Monedas actuales: {personaje.monedas}")
        if personaje.salud <= 0:
            print(f"{personaje.nombre} ha sido derrotado...")

def main():
    armero = Armero()
    mercader = Mercader()  # Creación de un mercader
    armero.agregar_arma(Arma("Espada", 15, "físico", 50))
    armero.agregar_arma(Arma("Hacha", 20, "físico", 75))
    armero.agregar_arma(Arma("Libro de Fuego", 25, "mágico", 100))
    armero.agregar_arma(Arma("Libro de Hielo", 20, "mágico", 90))

    print("Selecciona tu personaje:")
    print("1. Guerrero (Melee)")
    print("2. Mago")
    print("3. Personaje por defecto")
    eleccion = input("Tu elección: ")

    tipo_personaje = ""
    if eleccion == "1":
        tipo_personaje = "Melee"
    elif eleccion == "2":
        tipo_personaje = "Mago"
    elif eleccion == "3":
        tipo_personaje = "Defecto"
    else:
        print("Opción no válida.")
        return

    arma = elegir_arma(tipo_personaje)
    if arma:
        if tipo_personaje == "Melee":
            personaje = Melee("Guerrero", arma)
        elif tipo_personaje == "Mago":
            personaje = Mago("Mago", arma)
        elif tipo_personaje == "Defecto":
            personaje = PersonajePorDefecto("Defensor", arma)

        while True:
            print("\nMenú Principal:")
            print("1. Ir a combate")
            print("2. Ir al armero")
            print("3. Ir al mercader")
            print("4. Salir del juego")
            eleccion = input("Selecciona una opción: ")
            match eleccion:
                case "1":
                    enemigo = EnemigoComun()  # Puedes cambiar esto por otro tipo de enemigo.
                    combate(personaje, enemigo)
                case "2":
                    print("Armas disponibles en el armero:")
                    for i, arma in enumerate(armero.arsenal):
                        print(f"{i + 1}. {arma.nombre} (Daño: {arma.daño}, Precio: {arma.precio})")
                    print("Opciones del armero:")
                    print("1. Comprar arma")
                    print("2. Vender arma")
                    print("3. Mejorar arma")
                    eleccion_armero = input("Selecciona una opción: ")
                    match eleccion_armero:
                        case "1":
                            arma = elegir_arma(tipo_personaje)
                            if arma:
                                armero.vender_arma(arma, personaje)
                        case "2":
                            if personaje.arma:
                                armero.comprar_arma(personaje.arma, personaje)
                            else:
                                print("No tienes ninguna arma para vender.")
                        case "3":
                            if personaje.arma:
                                incremento = int(input("Cuánto deseas incrementar el daño del arma? "))
                                costo = int(input("Cuánto cuesta mejorar el arma? "))
                                armero.mejorar_arma(personaje.arma, personaje, incremento, costo)
                            else:
                                print("No tienes ninguna arma para mejorar.")
                        case _:
                            print("Opción no válida.")
                case "3":
                    mercader.mostrar_inventario()
                    eleccion_item = int(input("Selecciona un ítem para comprar: ")) - 1
                    if 0 <= eleccion_item < len(mercader.inventario):
                        mercader.vender_item(mercader.inventario[eleccion_item], personaje)
                    else:
                        print("Opción no válida.")
                case "4":
                    print("Gracias por jugar. ¡Hasta la próxima!")
                    break
                case _:
                    print("Opción no válida.")
                    
if __name__ == "__main__":
    main()