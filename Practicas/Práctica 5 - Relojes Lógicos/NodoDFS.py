import simpy
from Nodo import *
from Canales.CanalRecorridos import *
from random import randint

TICK = 1
class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, num_nodos):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = self.id_nodo # Cada nodo se inicializa como su propio padre
        self.hijos = []
        self.eventos = []
        self.reloj = [0] * num_nodos

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        # Tu implementación va aquí
        """
        Ejecuta el algoritmo de recorrido en profundidad (DFS).

        Args:
            env (simpy.Environment): Entorno de simulación de `simpy`.
        """
        if self.id_nodo == 0: # Nodo distinguido raíz
            #Elige el primer hijo de los vecinos
            self.hijos = [self.vecinos[0]]
            self.reloj[self.id_nodo] += 1
            recorridos = frozenset({self.id_nodo}) #Los nodos ya recorridos/visitados
            self.eventos.append((self.reloj.copy(), 'E', self.id_nodo, self.vecinos[0], recorridos))
            # Envía el mensaje GO 
            self.canal_salida.envia(("GO", recorridos, self.id_nodo, self.reloj.copy()), [self.vecinos[0]])
        
        while True:
            yield env.timeout(TICK)
            # Espera y recibe un mensaje
            msj = yield self.canal_entrada.get()
            (tipo, recorridos, j, reloj) = msj
            
            # Actualiza el reloj
            for i in range(len(self.reloj)):
                self.reloj[i] = max(reloj[i], self.reloj[i])
            self.reloj[self.id_nodo] += 1
            
            # Registra el evento de recepción
            self.eventos.append((self.reloj.copy(), 'R', j, self.id_nodo, recorridos))
            # Cuando recibe un mensaje GO establece al que se lo envió como su padre
            if tipo == "GO":
                self.padre = j
            
                # Revisa si ya visitó a  sus vecinos
                if set(self.vecinos) <= set(recorridos):
                    self.reloj[self.id_nodo] += 1
                    new_recorridos = frozenset(recorridos | {self.id_nodo})
                    self.eventos.append((self.reloj.copy(), 'E', self.id_nodo, j, new_recorridos))
                    
                    # Envía el mensaje BACK a su padre
                    self.canal_salida.envia(("BACK", new_recorridos, self.id_nodo, self.reloj.copy()), [j])
                
                else:
                    # Selelecciona el vecino no visitado con el identificador más pequeño
                    no_visitado = min(v for v in self.vecinos if v not in recorridos)
                    self.hijos = [no_visitado] 
                    self.reloj[self.id_nodo] += 1
                    new_recorridos = frozenset(recorridos | {self.id_nodo})
                    self.eventos.append((self.reloj.copy(), 'E', self.id_nodo, no_visitado, new_recorridos))
                    # Envía el mensaje GO al siguiente vecino no visitado
                    yield env.timeout(randint(1, 5))
                    self.canal_salida.envia(("GO", new_recorridos, self.id_nodo, self.reloj.copy()), [no_visitado])
            
            
            else:  
                # Si todos los vecinos ya fueron visitados
                if set(self.vecinos) <= set(recorridos):
                    if self.padre == self.id_nodo:  
                        return #termina el algoritmo
            
                    self.reloj[self.id_nodo] += 1
                    self.eventos.append((self.reloj.copy(), 'E', self.id_nodo, self.padre, recorridos))
                    yield env.timeout(TICK)
                    # Envía el mensaje BACK a su padre
                    self.canal_salida.envia(("BACK", recorridos, self.id_nodo, self.reloj.copy()), [self.padre])
                
                else:
                    #Encontra el siguiente vecino no visitado
                    no_visitado = min(v for v in self.vecinos if v not in recorridos)
                    self.hijos.append(no_visitado)
                    self.reloj[self.id_nodo] += 1
                    self.eventos.append((self.reloj.copy(), 'E', self.id_nodo, no_visitado, recorridos))
                    yield env.timeout(TICK)
                    
                    #Envía el mensaje GO
                    self.canal_salida.envia(("GO", recorridos, self.id_nodo, self.reloj.copy()),[no_visitado]) 
