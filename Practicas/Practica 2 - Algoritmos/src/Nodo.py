import simpy

class Nodo:
    """Representa un nodo.

    Cada nodo tiene un id, una lista de vecinos y dos canales de comunicación.
    Los métodos que tiene son únicamente getters.
    """
    def __init__(self, id_nodo: int, vecinos: list, canal_entrada: simpy.Store,
                 canal_salida: simpy.Store):
        '''Inicializa los atributos del nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida

    def get_id(self) -> int:
        '''Regresa el id del nodo.'''
        return self.id_nodo
    
    def get_vecinos(self) -> list:
        '''Regresa la lista de vecinos del nodo.'''
        return self.vecinos
    
    def get_canal_de_entrada(self) -> simpy.Store:
        '''Regresa el canal de entrada del nodo.'''
        return self.canal_entrada
    
    def get_canal_de_salida(self) -> simpy.Store:
        '''Regresa el canal de salida del nodo.'''
        return self.canal_salida
    
    def __str__(self) -> str:
        '''Regresa una representación en string del nodo.'''
        return f'Nodo: (ID: {self.id_nodo}), Vecinos: {self.vecinos}'
