import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo de consenso. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1) # Llenamos la lista de Nodos
        self.V[id_nodo] = id_nodo
        self.New = set([id_nodo])
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.

    def consenso(self, env, f):
        '''El algoritmo de consenso.'''
        # Aquí va su implementación
        
        #Los nodos que fallarán:
        if self.id_nodo < f:
            self.fallare = True
            
        # Comprueba si el conjunto `self.New` no está vacío. Si no lo está,
        # esperará usando `env.timeout(TICK)` antes de enviar
        # los mensajes a través del canal `self.canal_salida` a sus vecinos. El mensaje tendrá 
        # el conjunto `self.New` y el `id_nodo` del nodo que se enviará a todos los vecinos 
        # especificados en `self.vecinos`.
        
        if len(self.New) !=0:
            yield env.timeout(TICK)
            self.canal_salida.envia((self.New,self.id_nodo),self.vecinos) 

