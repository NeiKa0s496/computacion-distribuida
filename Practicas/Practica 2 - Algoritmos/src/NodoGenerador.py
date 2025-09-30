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
        self.mensajes_esperados = len(self.vecinos)
    
    def genera_arbol(self, env):
        #'''3.2 Algoritmo 4 – Construcción del árbol generador.'''
        # Si (0) es el nodo dsitinguido , inicia
        if self.id_nodo == 0: 
            self.padre = self.id_nodo # Enviamos GO a todos los vecinos
            self.mensajes_esperados = len(self.vecinos) #Los mensajes que espera recibir sean vecinos
            yield env.timeout(TICK) #en Simpy dice que es una instrucción que pausa la ejecución por un tiempo determinado.
            self.canal_salida.envia(["GO", self.id_nodo], self.vecinos)
        
        # Procesamos mensajes entrantes
        while True:
            mensaje = yield self.canal_entrada.get()
        # Explicación 
        # El nodo distinguido envía GO() a sus vecinos. Cada nodo que recibe un GO por primera vez
        # establece a su padre y reenvía el mensaje. Cuando un nodo ha recibido todas las respuestas,
        # envía un BACK a su padre.
            # Primera vez que recibe GO
            if mensaje [0] == "GO":
                if self.padre is None: 
                    self.padre = mensaje[1] # Asignamos como nodo padre al nodo que envió el mensaje GO
                    self.mensajes_esperados = len(self.vecinos) - 1
                    
                    if self.mensajes_esperados == 0:
                        yield env.timeout(TICK)
                        # Enviamos un mensaje BACK al nodo que previamente le mandó msj y que sabemos se convirtió en su padre
                        self.canal_salida.envia(["BACK", self.id_nodo], [self.padre])
                    else:
                        yield env.timeout(TICK)
                        # Continuamos enviando mensaje GO a sus demás vecinos (a excepción del nodo que le mandó el mensaje)
                        self.canal_salida.envia(["GO", self.id_nodo], [v for v in self.vecinos if v != self.padre])
                else:
                    # Si ya tiene un nodo padre asignado 
                    yield env.timeout(TICK)
                    # -1 indica que ya se ha asignado un nodo padre 
                    self.canal_salida.envia(["BACK", -1], [mensaje[1]])
                        
            
            # SI SE RECIBE UN MENSAJE BACK
            elif mensaje[0] == "BACK":
                self.mensajes_esperados -= 1
                
                if mensaje[1] != -1:
                    # El nodo que envió el mensaje back, es hijo del nodo actual
                    self.hijos.append(mensaje[1]) 
                    
                if self.mensajes_esperados == 0:
                    if self.padre != self.id_nodo:
                        yield env.timeout(TICK)
                        # Se mandan mensajes BACK a los nodos padres, hasta llegar al nodo distinguido
                        self.canal_salida.envia(["BACK", self.id_nodo], [self.padre])
                    else:
                        # El nodo distinguido recibió el último mensaje BACK
                        break