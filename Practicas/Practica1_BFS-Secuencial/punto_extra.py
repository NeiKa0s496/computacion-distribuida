import queue
from bfs_secuencial import bfs


def crear_grafo_desde_input():
    """
    Función para crear un grafo a partir de input del usuario con el mismo formato que bfs_secuencial.py
    """
    grafica = {}
    while True:
        entrada = input(" > ").strip()
        if entrada == "":
            break

        if ":" not in entrada:
            print("Usa el formato: nodo: nodo1,nodo2,nodo3")
            continue

        nodo, nodos_str = entrada.split(":", 1)
        nodo = nodo.strip()
        
        # normaliza los vecinos
        nodo_v = [v.strip() for v in nodos_str.split(",") if v.strip()]
        
        if not nodo_v:
            print("Debe haber al menos un vecino")
            continue

        # Agrega el nodo y sus vecinos
        if nodo in grafica:
            for vecino in nodo_v:
                if vecino not in grafica[nodo]:
                    grafica[nodo].append(vecino)
        else:
            grafica[nodo] = nodo_v
        
        # Ve si los vecinos también son nodos en el grafo
        for vecino in nodo_v:
            if vecino not in grafica:
                grafica[vecino] = []
                
    grafica = grafica.copy()
    for nodo, vecinos in grafica.items():
        for vecino in vecinos:
            if nodo not in grafica[vecino]:
                grafica[vecino].append(nodo)
                
    return grafica 

def es_grafo_conexo(grafica):
    """
    Verifica si el grafo es conexo usando BFS
    """
    if not grafica:
        return False

    # Toma un nodo para iniciar 
    nodo_inicio = next(iter(grafica.keys()))

    # BFS para ver si son conexas
    cola = queue.Queue()
    visitados = set()

    cola.put(nodo_inicio)
    visitados.add(nodo_inicio)

    while not cola.empty():
        nodo_actual = cola.get()
        for vecino in grafica[nodo_actual]:
            if vecino not in visitados:
                visitados.add(vecino)
                cola.put(vecino)

    # El grafo es conexo si podemos visitar todos los nodos
    return len(visitados) == len(grafica)


def main():
    """
    Función principal que maneja la interacción con el usuario
    """
    print("=== ALGORITMO BFS PARA GRÁFICAS CONEXAS ===")
    print("Formato de entrada: nodo: nodo1,nodo2,nodo3")
    print("Enter sin ingresar nada para terminarlo\n")

    while True:
        grafica = crear_grafo_desde_input()
        
        if not grafica:
            print("El grafo está vacío.")
            continue
        
        if not es_grafo_conexo(grafica):
            print(" El grafo no es conexo.")
            print("Ingresa un grafo conexo.")
            continue
        break

    # gr'afica completa
    print(f"\n Gráfica :")
    for nodo, vecinos in sorted(grafica.items()):
        print(f"  {nodo}: {', '.join(sorted(vecinos))}")

    # Nodos disponibles
    nodos = list(grafica.keys())
    print(f"\nNodos disponibles: {', '.join(sorted(nodos))}")

    # Pide el nodo inicial
    while True:
        nodo_inicio = input("\nEl nodo para iniciar: ").strip()
        if nodo_inicio in grafica:
            break
        else:
            print(f"'{nodo_inicio}' no existe")


    # BFS
    resultado = bfs(grafica, nodo_inicio)

    # Resultados
    print("\n" + "=" * 50)
    print("=" * 50)
    print(f"Recorrido desde '{nodo_inicio}': {resultado}")

if __name__ == "__main__":
    main()