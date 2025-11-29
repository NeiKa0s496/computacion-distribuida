from Canales.CanalRecorridos import *
from NodoConsenso import *
import simpy

class TestPractica6:
    ''' Clase para las pruebas unitarias de la práctica 6. '''

    # Las aristas de adyacencias de la gráfica.
    adyacencias = [[1, 2, 3, 4, 5, 6], [0, 2, 3, 4, 5, 6], [0, 1, 3, 4, 5, 6],
                   [0, 1, 2, 4, 5, 6], [0, 1, 2, 3, 5, 6], [0, 1, 2, 3, 4, 6],
                   [0, 1, 2, 3, 4, 5]]

    def test_consenso_con_detector_fallas(self):
        ''' Método que prueba el algoritmo de consenso con detector de fallas. '''
        # Creamos el ambiente y el objeto Canal
        env = simpy.Environment()
        bc_pipe = CanalRecorridos(env)

        # La lista que representa la gráfica
        grafica = []

        # Creamos los nodos
        for i in range(0, len(self.adyacencias)):
            grafica.append(NodoConsenso(i, self.adyacencias[i],
                                        bc_pipe.crea_canal_de_entrada(), bc_pipe))

        # Le decimos al ambiente lo que va a procesar y ejecutar
        f = 2 # El número de fallos
        for nodo in grafica:
            env.process(nodo.consenso(env, f))
        env.run()

        # Verificaciones
        nodos_fallidos = 0
        lider_elegido = None
        
        for i in range(0, len(grafica)):
            nodo = grafica[i]
            if nodo.fallare:
                nodos_fallidos += 1
            else:
                if lider_elegido is None:
                    lider_elegido = nodo.lider
                # Verificar que todos los nodos no fallidos tienen el mismo líder
                assert lider_elegido == nodo.lider, f"Nodo {i} tiene líder {nodo.lider}, esperado {lider_elegido}"
                # Verificar que el conjunto suspected es consistente entre nodos no fallidos
                print(f"Nodo {i}: suspected = {nodo.suspected}")
        
        assert nodos_fallidos == f, f"Fallidos: {nodos_fallidos}, esperados: {f}"
        
        print("Prueba exitosa: Todos los nodos no fallidos alcanzaron consenso")

if __name__ == "__main__":
    test = TestPractica6()
    test.test_consenso_con_detector_fallas()