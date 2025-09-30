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
        self.recibido = set 
        self.recibio_mensaje = False

    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        # Tú código aquí
        
        # Si el nodo es distinguido (0) inicia
        if self.id_nodo == 0 and self.mensaje is not None and not self.recibio_mensaje:
            self.recibio_mensaje = True
            # Enviamos el mensaje a todos los vecinos
            yield env.timeout(TICK)
            self.canal_salida.envia(("GO", self.mensaje), self.vecinos)
        
        # Procesamos mensajes entrantes
        while True:
            mensaje = yield self.canal_entrada.get()
            
            if isinstance(mensaje, tuple) and mensaje[0] == "GO":
                _, data = mensaje
                if not self.recibio_mensaje:
                    self.recibio_mensaje = True
                    self.mensaje = data
                    
                    # Reenviamos el mensaje a los vecinos
                    if self.vecinos:  # Si tenemos vecinos
                        yield env.timeout(TICK)
                        self.canal_salida.envia(("GO", data), self.vecinos)
