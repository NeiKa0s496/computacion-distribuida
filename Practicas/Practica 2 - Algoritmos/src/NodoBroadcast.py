import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

# La unidad de tiempo
TICK = 1


class NodoBroadcast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje
        self.recibido = set()
        self.recibio_mensaje = False

    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        # Tú código aquí
        
        # Si el nodo es distinguido (0) inicia
        if self.id_nodo and self.mensaje == 0:
            print(f'Tiempo {env.now}: Nodo {self.id_nodo} envia mensaje "{self.mensaje}"')
            
            # Envía el mensaje a los demás nodos
            yield env.timeout(TICK)
            for vecino in self.vecinos:
                self.canal_salida.envia((self.id_nodo, self.mensaje), [vecino])
        
        # Procesa lso mensajes entrantes
        while True:
            mensaje = yield self.canal_entrada.get()
            nodo_emisor, contenido = mensaje
            
            # Si es un mensaje nuevo
            if nodo_emisor not in self.recibido:
                self.recibido.add(nodo_emisor)
                self.recibio_mensaje = True
                self.mensaje = contenido
                
                print(f'Tiempo {env.now}: Nodo {self.id_nodo} recibe mensaje "{contenido}" del Nodo {nodo_emisor}')
                
                # Reenvía excepto a 0
                vecinos_a_reenviar = [v for v in self.vecinos if v != nodo_emisor]
                if vecinos_a_reenviar:
                    yield env.timeout(TICK)
                    for vecino in vecinos_a_reenviar:
                        self.canal_salida.envia((self.id_nodo, contenido), [vecino])
            
            yield env.timeout(TICK) 