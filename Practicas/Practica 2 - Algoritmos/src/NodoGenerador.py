import simpy
from Nodo import *
from Canales.CanalBroadcast import *

TICK = 1

class NodoGenerador(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de flooding.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos propios del algoritmo
        self.padre = None if id_nodo != 0 else id_nodo # Si es el nodo distinguido, el padre es el mismo 
        self.hijos = list()
        self.mensajes_esperados = len(vecinos) # Cantidad de mensajes que esperamos
        self.recibio_go = False 
        self.expected_msgs = 0
    
    def genera_arbol(self, env):
        '''3.2 Algoritmo 4 – Construcción del árbol generador.'''
        # Si (0) es el nodo dsitinguido , inicia
        if self.id_nodo == 0: 
            self.padre = self.id_nodo
            # Enviamos GO a todos los vecinos 
            yield env.timeout(TICK) #en Simpy dice que es una instrucción que pausa la ejecución por un tiempo determinado.
            self.canal_salida.envia("GO", self.vecinos)
        
        # Procesamos mensajes entrantes
        while True:
            mensaje = yield self.canal_entrada.get()
            # Extraemos el tipo de mensaje que recibimos
            mensaje = mensaje[1]
            
        # Explicación 
        # El nodo distinguido envía GO() a sus vecinos. Cada nodo que recibe un GO por primera vez
        # establece a su padre y reenvía el mensaje. Cuando un nodo ha recibido todas las respuestas,
        # envía un BACK a su padre.
            
            if mensaje == "GO":
                if not self.recibio_go:  # Primera vez que recibe GO
                    self.recibio_go = True
                    self.padre = 0
                    
                    # Reenviamos GO 
                    vecinos_para_reenviar = [v for v in self.vecinos if v != self.padre]
                    self.mensajes_esperados = len(vecinos_para_reenviar)
                    
                    if vecinos_para_reenviar:
                        yield env.timeout(TICK)
                        self.canal_salida.envia("GO", vecinos_para_reenviar)
                    else:
                        # Si no tenemos vecinos para reenviar, enviamos BACK a nuestro padre
                        yield env.timeout(TICK)
                        self.canal_salida.envia(("BACK", self.id_nodo), [self.padre])
                else:
                    # enviamos BACK
                    yield env.timeout(TICK)
                    self.canal_salida.envia(("BACK", None), [self.padre])
            
            elif isinstance(mensaje, tuple) and mensaje[0] == "BACK":
                _, val_set = mensaje
                self.mensajes_esperados -= 1
                
                if val_set is not None:
                    self.hijos.append(val_set)
                
                if self.mensajes_esperados == 0 and self.id_nodo != 0:
                    # Enviamos BACK al padre
                    yield env.timeout(TICK)
                    self.canal_salida.envia(("BACK", self.id_nodo), [self.padre])