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
        
        # Determinar los nodos que fallarán
        if self.id_nodo < f:
            self.fallare = True
            return
        
        ronda = 0
        valor = self.id_nodo  # Valor inicial 
        valores_recibidos = set([valor])
        n_rondas = f + 1

        for ronda in range(n_rondas):
            # Si el nodo falla en esta ronda o después, no participa
            if self.fallare and ronda >= f:
                break

            # Mensaje (id del nodo, valor propuesto, número de ronda)
            if self.New:
                yield self.canal_salida.envia((self.id_nodo, valor, ronda), self.vecinos)
            
            self.New = set()
            yield env.timeout(TICK)  # Esperar con TICK
            mensajes_ronda = []
            
            # Recibir mensajes del canal de entrada
            while len(self.canal_entrada.items) > 0:
                    mensaje = yield self.canal_entrada.get()
                    id_remitente, valor_remitente, ronda_mensaje = mensaje
                    if ronda_mensaje == ronda:
                        mensajes_ronda.append(valor_remitente)
                        self.V[id_remitente] = (
                            id_remitente  # Actualiza V con el id del remitente
                        )
            yield env.timeout(0.01)

            # Actualizar los valores recibidos
            valores_recibidos.update(mensajes_ronda)

            # el valor propuesto es el mínimo recibido
            valor = min(valores_recibidos)
            ronda += 1

        # Al finalizar, elige el líder
        self.lider = next(item for item in self.V if item is not None)