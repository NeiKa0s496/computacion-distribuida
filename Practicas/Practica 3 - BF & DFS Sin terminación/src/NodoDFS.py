import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        # Tu implementación va aquí
        self.id_nodo = id_nodo
        self.vecinos = set(vecinos)
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos para DFS
        self.padre = id_nodo if id_nodo == 0 else None
        self.hijos = []
        self.visitados = set()
        self.estado = "NO_VISITADO"

    def dfs(self, env):
        ''' Algoritmo DFS. '''
        # Tu implementación va aquí
        
        # when start() is received do (solo p_0 recibe este mensaje)
        if self.id_nodo == 0:
            # parent_i ← i osea se establece como su propio padre
            self.padre = self.id_nodo
            self.visitados.add(self.id_nodo)
            
            # let k ∈ neighbors_i; send GO([i]) to p_k; children_i ← {k}
            if self.vecinos:
                k = min(self.vecinos) #escojo el vecino menor porque se puede dar a entender eso en los test
                yield env.timeout(TICK)
                self.canal_salida.envia(["GO", self.id_nodo, [self.id_nodo]], [k])
                self.hijos = [k]
        
        while True:
            mensaje = yield self.canal_entrada.get()
            tipo = mensaje[0]
            remitente = mensaje[1]  # p_j
            visitados_recibidos = set(mensaje[2])  # visited
            
            # when GO(visited) is received from p_j do
            if tipo == "GO":
                # parent_i ← j
                self.padre = remitente
                self.visitados.update(visitados_recibidos)
                self.visitados.add(self.id_nodo)
                
                #if (neighbors_i ⊆ visited)
                vecinos_no_visitados = [v for v in self.vecinos if v not in self.visitados]
                
                if not vecinos_no_visitados:
                    # send BACK(visited ∪ {i}) to p_j; children_i ← ∅
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["BACK", self.id_nodo, self.visitados.copy()], [self.padre])
                    self.hijos = []
                else:
                    # let k ∈ neighbors_i \ visited; send GO(visited ∪ {i}) to p_k; children_i ← {k}
                    k = min(vecinos_no_visitados)
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["GO", self.id_nodo, self.visitados.copy()], [k])
                    self.hijos = [k]
            
            # when BACK(visited) is received from p_j do
            elif tipo == "BACK":
                self.visitados.update(visitados_recibidos)
                
                # if (neighbors_i ⊆ visited)
                vecinos_no_visitados = [v for v in self.vecinos if v not in self.visitados]
                
                if not vecinos_no_visitados:
                    # if (parent_i = i) then
                    if self.padre == self.id_nodo:
                        # the traversal is terminated
                        print(f"DFS completado desde la raíz {self.id_nodo}")
                        break
                    else:
                        # send BACK(visited) to p_parent_i
                        yield env.timeout(TICK)
                        self.canal_salida.envia(["BACK", self.id_nodo, self.visitados.copy()], [self.padre])
                else:
                    # let k ∈ neighbors_i \ visited; send GO() to p_k; children_i ← children_i ∪ {k}
                    k = min(vecinos_no_visitados)
                    yield env.timeout(TICK)
                    self.canal_salida.envia(["GO", self.id_nodo, self.visitados.copy()], [k])
                    self.hijos.append(k)
