from abc import ABC
import random
from typing import List, Optional

from Excepciones import PersonajeNoTieneItemError

class Item:
    def __init__(self, nombre: str, efecto: str, cantidad: int, precio: int):
        self.nombre: str = nombre
        self.efecto: str = efecto
        self.cantidad: int = cantidad
        self.precio: int = precio

    def usar(self, personaje: 'Personaje', enemigo: 'Enemigo' = None) -> str:
        
        if self.efecto == "curación":
            personaje.salud += self.cantidad
            
        elif self.efecto == "revitalizar energía":
            personaje.energia += self.cantidad
            
        elif self.efecto == "envenenar enemigo" and enemigo is not None:
            enemigo.salud -= self.cantidad

class Arma:
    def __init__(self, nombre: str, daño: int, tipo: str, precio: int) -> None:
        self.nombre: str = nombre
        self.daño: int = daño
        self.tipo: str = tipo
        self.precio: int = precio

class Personaje(ABC):
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
        self.arma: Optional[Arma] = arma
        self.monedas: int = monedas
        self.habilidades: List[str] = habilidades if habilidades is not None else []
        self.inventario: List[Item] = inventario if inventario is not None else [
            Item("Curación", "curación", 20, 30),
            Item("Revitalizar Energía", "revitalizar energía", 20, 30),
            Item("Veneno", "envenenar enemigo", 10, 30)
        ]

    def atacar(self, enemigo: 'Enemigo') -> None:
        raise NotImplementedError

    def defender(self) -> None:
        self.salud = self.salud + ((self.defensa_fisica + self.defensa_magica)/2)

    def usar_item(self, item: Item, enemigo: Optional['Enemigo'] = None) -> None:
        if item in self.inventario:
            item.usar(self, enemigo)
            indice = self.inventario.index(item)
            self.inventario[indice].cantidad -= 1
        else:
            raise PersonajeNoTieneItemError()


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
            daño_normal: int = max(self.daño_fisico + self.arma.daño - enemigo.defensa_fisica, 0)
            enemigo.salud -= daño_normal
            return daño_normal
        elif evento == "critico":
            daño_critico: int = max(2 * (self.daño_fisico + self.arma.daño) - enemigo.defensa_fisica, 0)
            enemigo.salud -= daño_critico
            return daño_critico
        else:
            return 0

        

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
        evento: str = random.choice(["normal", "critico", "fallo"])
        if evento == "normal":
            daño_normal: int = max(self.daño_magico + self.arma.daño - enemigo.defensa_magica, 0)
            enemigo.salud -= daño_normal
            self.energia -= 10
            return daño_normal
        elif evento == "critico":
            daño_critico: int = max(2 * (self.daño_magico + self.arma.daño) - enemigo.defensa_magica, 0)
            enemigo.salud -= daño_critico
            self.energia -= 10
            return daño_critico
        else:
            return 0
            
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
        evento: str = random.choice(["normal", "critico", "fallo"])
        if evento == "normal":
            daño_normal: int = max(self.daño_fisico + self.arma.daño - enemigo.defensa_fisica, 0)
            enemigo.salud -= daño_normal
            return daño_normal
        elif evento == "critico":
            daño_critico: int = max(2 * (self.daño_fisico + self.arma.daño) - enemigo.defensa_fisica, 0)
            enemigo.salud -= daño_critico
            return daño_critico
        else:
            return 0
        
class Enemigo(ABC):
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

    def atacar(self, personaje: 'Personaje') -> None:
        daño_real: int = max(self.daño_fisico - personaje.defensa_fisica, 0)
        personaje.salud -= daño_real
        return daño_real

    def defender(self) -> None:
        defensa = ((self.defensa_fisica + self.defensa_magica)/2)
        self.salud = self.salud + defensa
        return defensa

    def usar_habilidad(self, personaje: 'Personaje') -> None:
        NotImplementedError

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
        self.arsenal: dict[str][Arma] = {
        "Melee": [Arma("Doble Espada", 30, "físico", 100), Arma("Martillo", 40, "físico", 150)],
        "Mago": [Arma("Hoz Ardiente", 50, "mágico", 180), Arma("Heladura", 40, "mágico", 150)],
        "Defecto": [Arma("Puños", 5, "físico", 0)]
    }
        
    def agregar_arma(self, arma: Arma, tipo_personaje: str) -> None:
        self.arsenal[tipo_personaje].append(arma)

    def vender_arma(self, arma: Arma, personaje: Personaje, tipo_personaje) -> bool:
        if personaje.monedas >= arma.precio:
            personaje.monedas -= arma.precio
            personaje.arma = arma
            indice_arma = self.arsenal[tipo_personaje].index(arma)
            del self.arsenal[tipo_personaje][indice_arma]
            return True 
        else:
            return None

    def comprar_arma(self, arma: Arma, personaje: Personaje, tipo_personaje: str) -> bool:
        if personaje.arma == arma:
            personaje.monedas += arma.precio
            self.arsenal[tipo_personaje].append(arma)
            personaje.arma = Arma("Puños", 5, "físico", 0)
            return True

    def mejorar_arma(self, arma: Arma, personaje: Personaje) -> bool:
        _incremento = 10
        _costo = 75
        if personaje.monedas >= _costo:
            arma.daño += _incremento
            personaje.monedas -= _costo
            return True     
        else:
            return None
            
class Mercader:
    def __init__(self) -> None:
        self.inventario: List[Item] = [
            Item("Curación", "curación", 20, 30),
            Item("Revitalizar Energía", "revitalizar energía", 20, 30),
            Item("Veneno", "envenenar enemigo", 10, 30)
        ]

    def vender_item(self, item: Item, personaje: Personaje) -> bool:
        if personaje.monedas >= item.precio:
            personaje.monedas -= item.precio
            personaje.inventario.append(item)
            indice = self.inventario.index(item)
            self.inventario[indice].cantidad -= 1
            return True
        else:
            return False