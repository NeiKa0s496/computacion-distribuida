import queue

#Árbol A
grafica = {
    'A': ['B', 'C', 'D', 'E'],
    'B': ['A', 'C', 'G'],
    'C': ['A', 'B', 'D'],
    'D': ['H', 'E', 'A', 'C'],
    'E': ['A', 'D', 'F'],
    'F': ['G', 'E', 'H', 'I'],
    'G': ['F', 'B'],
    'H': ['F', 'D'],
    'I': ['F']
}

def bfs(grafica, nodo_inicio):
    """
    Implementación del algoritmo Breadth-First Search (BFS)
    
    Args:
        grafica : El árbol A de ejemplo 
        nodo_inicio (str): Nodo desde donde se inicia el recorrido BFS
    
    Returns:
        list: Lista con los nodos visitados en orden correcto BFS
    """
    
    visitados = set()
    cola = queue.Queue()
    
    # Agregar nodo inicial a la cola y marcarlo como visitado
    cola.put(nodo_inicio)
    visitados.add(nodo_inicio)
    n_visitado = []
    
    while not cola.empty():
        # Saca el primer nodo de la cola
        nodo_actual = cola.get()
        n_visitado.append(nodo_actual)
        
        # Obtenemso todos los nodos del nodo actual
        if nodo_actual in grafica:
            nodo_v = grafica[nodo_actual]
            
            # Si el nodo no ha sido visitado, se agrega a la cola
            for vecino in nodo_v:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.put(vecino)
    
    return n_visitado

# Probar con árbol A (por lo del requsito 1 del pdf)
if __name__ == "__main__":
    resultado = bfs(grafica, 'A') #Llamamos a la funcion bfs
    print("Recorrido BFS desde 'A':", resultado)