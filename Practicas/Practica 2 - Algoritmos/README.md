# Practica 2: Algoritmos en Computación Distribuida

## Profesor : Mauricio Riva Palacio Orozco
## Ayudantes:
- Adrián Felipe Fernández Romero
- Alan Alexis Martínez López
<p>

## Tabla de Contenidos
- [1. Introducción](#1-introducción)
- [2. Objetivos](#2-uso)
- [3. Estructura de la práctica](#3-estructura)
- [4. Explicación de la implementación](#4-implementacion)

## **1. Introducción**
En esta práctica se busca que los alumnos implementen algunos de los algoritmos
fundamentales en computación distribuida, utilizando Simpy para simular la comunicación
entre procesos. El objetivo es comprender cómo los procesos (nodos) en una red pueden: 
- 1) Conocer a los vecinos de sus vecinos
- 2) Construir un árbol generador a partir de un nodo
distinguido
- 3) Difundir (broadcast) un mensaje desde un nodo raíz a toda la red.

## **2. Uso**
### En una terminal :
- Generamos el entorno virtual

```bash
python3 -m venv venv
```
- Activamos el entorno:
```bash
 source venv/bin/activate
```
- Paquetes:
```bash
pip install -r requirements.txt
```
- Ejecutar Tests con:
```bash
pytest src/test.py
```
## **3. Estructura**
## Estructura de la práctica

```plaintext
README.md
requirements.txt                   
src
├── Canales/                 # Sistema de comunicación entre nodos
│   ├── CanalBroadcast.py
│   └── Canal.py
├── Nodo.py                  # Clase base para todos los nodos
├── NodoBroadcast.py         # Implementación del algoritmo Broadcast
├── NodoGenerador.py         # Implementación del árbol generador
├── NodoVecinos.py           # Implementación para conocer vecinos
└── test.py
```
## **4. Implementación**
### Broadcast (NodoBroadcast.py)

El nodo distinguido con ID = 0 envía un mensaje que debe llegar a todos los nodos de la red.

1. **Inicialización del nodo distinguido:**
   - El nodo 0 comienza con un mensaje predefinido
   - Marca que ha recibido el mensaje (`recibio_mensaje = True`)
   - Se agrega a sí mismo al conjunto de nodos procesados (`recibido`)

2. **Envío inicial:**
   - El nodo 0 espera un TICK
   - Envía el mensaje a todos sus vecinos en formato `(id_emisor, contenido)`

3. **Procesamiento de mensajes entrantes:**
   - Cada nodo espera mensajes en su canal de entrada
   - Al recibir un mensaje, extrae el ID del emisor y el contenido
   - Verifica si ya había recibido mensaje de ese emisor (evita ciclos)

4. **Reenvío:**
   - Si es un mensaje nuevo (emisor no está en `recibido`):
     - Agrega el emisor al conjunto `recibido`
     - Guarda el mensaje
     - Calcula vecinos a quienes reenviar (todos excepto el emisor)
     - Espera un TICK y reenvía el mensaje a esos vecinos

5. **Terminación:**
   - El algoritmo continúa hasta que no hay más mensajes nuevos
   - Todos los nodos habrán recibido el mensaje original

### Arbol Generador (NodoGenerador.py)

El algoritmo construye el árbol en dos fases, una de exploración con los mensajes GO y una de confirmación con mensajes BACK.


1. **Inicialización del nodo distinguido:**
   - El nodo 0 se establece como su propio padre
   - Calcula cuántos mensajes BACK debe esperar (número de vecinos)
   - Envía mensaje ("GO", 0) a todos sus vecinos

2. **Recepción del primer GO:**
   - Cuando un nodo recibe su primer mensaje GO:
     - Establece al emisor como su padre `(self.padre = emisor)`
     - Marca que ya recibió GO `(recibio_go = True)`
     - Calcula vecinos para explorar (todos excepto su padre)
     - Establece contador de mensajes esperados

3. **Propagación de GO:**
   - Si tiene vecinos para explorar:
     - Envía `("GO", self.id_nodo)` a cada vecino no explorado
     - Espera sus respuestas BACK
   - Si es una hoja:
     - Envía inmediatamente `("BACK", self.id_nodo)` a su padre
   - En caso de repetidos, si un nodo recibe un GO adicional, responde con `("BACK", none)`, indicando que ya tiene padre

4. **Recepción de BACK:**
   - Decrementa el contador de mensajes esperados
   - Si `hijo_id` no es `None`, lo agrega a su lista de hijos
   - Si ya recibió todos los BACK esperados:
     - Envía su propio BACK al padre
     - El nodo distinguido termina cuando recibe todos los BACK

5. **Terminación:**
   - El algoritmo termina cuando el nodo 0 ha recibido todos los BACK
   - Cada nodo conoce su posición en el árbol

### Conocer vecinos (NodoVecinos.py)

Cada nodo aprende quienes son los vecinos de sus vecinos, conociendo la topologia local de la red.

1. **Fase de Envío:**
   - Cada nodo envía su lista completa de vecinos a todos sus vecinos.
   - Esto ocurre simultáneamente en todos los nodos.

2. **Fase de Recepción:**
   - Cada nodo escucha en su canal de entrada.
   - Por cada mensaje recibido (lista de vecinos):
     - Agrega todos los IDs a su conjunto `identifiers`.
     - Usa `set.update()` para agregar múltiples elementos.

3. **Conocimiento de la red:**
   - El conjunto `identifiers` crece conforme llegan mensajes.
   - Incluye:
     - Los vecinos directos del nodo.
     - Los vecinos de cada vecino directo.
   - No incluye necesariamente al nodo mismo.

4. **Terminación:**
   - El algoritmo termina cuando todos los nodos han enviado sus listas.
   - Cada nodo habrá recibido información de todos sus vecinos.