import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1


class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        # Aquí va tu implementacion '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos para BFS
        self.padre = self.id_nodo if id_nodo == 0 else None # parent_i = ⊥ para i ≠ 0
        self.hijos = []  # children_i = ∅
        self.distancia = 0 if id_nodo == 0 else float('inf') # level_i = ∞ para i ≠ 0
        self.msj_esperados = 0 # expected_msg_i = 0
        self.nivel = 0

    def bfs(self, env):
        ''' Algoritmo BFS. '''
        # Tu implementacion va aqui abajp
        
         # Línea 1: when start() is received do (proceso distinguido)
        if self.id_nodo == 0:
            # Inicia del nodo raíz (osea start())
            self.padre = self.id_nodo
            self.distancia = 0
            self.nivel = 0
            self.msj_esperados = len(self.vecinos)  # los vencinos neighbors_i
            
            if self.msj_esperados > 0:
                yield env.timeout(TICK)
                # send go(-1) to itself (nosotros enviamos go(0) a vecinos)
                self.canal_salida.envia(["GO", self.id_nodo, self.nivel], self.vecinos)
            
        while True:
            mensaje = yield self.canal_entrada.get()
            tipo = mensaje[0]
            remitente = mensaje[1]  # p_j
            nivel_recibido = mensaje[2]  # d
            
            # when go(d) is received from p_j do
            if tipo == "GO":
                # if (parent_i=⊥)
                if self.padre is None:
                    #parent_i ← j; children_i ← ∅; level_i ← d+1
                    self.padre = remitente
                    self.hijos = []
                    self.nivel = nivel_recibido + 1
                    self.distancia = nivel_recibido + 1
                    
                    # expected_msg_i ← neighbors_i \ {j}
                    vecinos_sin_padre = [vecino for vecino in self.vecinos if vecino != self.padre]
                    self.msj_esperados = len(vecinos_sin_padre)
                    
                    # if (expected_msg_i = 0) then... else...
                    if self.msj_esperados == 0:
                        # send back(yes, d+1) to p_parent
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["BACK", self.id_nodo, "yes", self.nivel], [self.padre])
                    else:
                        # for each k ∈ neighbors_i \ {j} do send go(d+1) to p_k
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["GO", self.id_nodo, self.nivel], vecinos_sin_padre)
                        
                # else if (level_i > d+1)
                elif self.nivel > nivel_recibido + 1:
                    # parent_i ← j; children_i ← ∅; level_i ← d+1
                    self.padre = remitente
                    self.hijos = []
                    self.nivel = nivel_recibido + 1
                    self.distancia = nivel_recibido + 1
                    
                    # expected_msg_i ← |neighbors_i \ {j}|
                    vecinos_sin_padre = [vecino for vecino in self.vecinos if vecino != self.padre]
                    self.msj_esperados = len(vecinos_sin_padre)
                    
                    #if (expected_msg_i = 0)
                    if self.msj_esperados == 0:
                        #send back(yes, level_i) to p_parent
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["BACK", self.id_nodo, "yes", self.nivel], [self.padre])
                    else:
                        #for each k ∈ neighbors_i \ {j} do send go(d+1) to p_k
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["GO", self.id_nodo, self.nivel], vecinos_sin_padre)
                else:
                    #else send back(no, d+1) to p_j
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["BACK", self.id_nodo, "no", nivel_recibido + 1], [remitente])

            #when back(resp, d) is received from p_j do
            elif tipo == "BACK":
                remitente = mensaje[1]  # p_j
                respuesta = mensaje[2]  # resp
                nivel_back = mensaje[3]  # d
                
                #if (d = level_i + 1)
                if nivel_back == self.nivel + 1:
                    #then if (resp = yes) then children_i ← children_i ∪ {j}
                    if respuesta == "yes":
                        self.hijos.append(remitente)
                    #expected_msg_i ← expected_msg_i - 1
                    self.msj_esperados -= 1
                    
                    #if (expected_msg_i = 0) then
                    if self.msj_esperados == 0:
                        #if (parent_i ≠ i) then send back(yes, level_i) to p_parent
                        if self.padre != self.id_nodo:
                            yield env.timeout(TICK)
                            self.canal_salida.envia(["BACK", self.id_nodo, "yes", self.nivel], [self.padre])
                        else:
                            #else p_i learns that the breadth-first tree is built
                            print(f"El nodo raíz {self.id_nodo} sabe que el algoritmo BFS ha terminado")
                            break