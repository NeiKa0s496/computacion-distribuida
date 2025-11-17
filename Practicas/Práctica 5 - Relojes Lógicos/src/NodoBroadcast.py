import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint

class NodoBroadcast(Nodo):
    def __init__(self, id_nodo: int, vecinos: list, canal_entrada: simpy.Store,
                 canal_salida: simpy.Store):
        super().__init__(id_nodo,vecinos,canal_entrada,canal_salida)
        self.mensaje = None
        self.reloj = 0
        self.eventos = []

    def broadcast(self, env: simpy.Environment, data="Mensaje"):
        #Tu implementacion va aqui
        """
        Envia un mensaje a los nodos vecinos y los recibe.
        
        Args:
            env (simpy.Environment): Entorno de simulación de `simpy`.
            data (str, optional): El mensaje que se va a transmitir: "Mensaje".
        """
        if self.mensaje != 0:
            self.mensaje = None
        
        if self.id_nodo == 0:
            self.mensaje = data
            evento = 'E'
            yield env.timeout(randint(1,5))
            
            #envia el mensaje a los vecinos
            for k in self.vecinos:
                self.reloj += 1
                self.eventos.append([self.reloj, evento, data, self.id_nodo, k])
                self.canal_salida.envia((data, self.reloj, self.id_nodo),[k])

        yield env.timeout(randint(1,5))

        while True:
            yield env.timeout(randint(1,5))
            evento = 'R'
            
        # recibe el mensaje de un vecino
            (data, reloj, j) = yield self.canal_entrada.get()
            self.reloj = max(self.reloj, reloj) + 1
            self.eventos.append([self.reloj, evento, data, j, self.id_nodo])
            #el mensaje recibido se procesa
            self.mensaje = data
            yield env.timeout(randint(1,5))
            
            #envia el mensaje a los vecinos
            for k in self.vecinos:
                self.reloj += 1
                self.eventos.append([self.reloj,'E',data,self.id_nodo,k])
                self.canal_salida.envia((data,self.reloj,self.id_nodo),[k])