# Práctica 5: Relojes Lógicos

## Profesor : Mauricio Riva Palacio Orozco
## Ayudantes:
- Adrián Felipe Fernández Romero
- Alan Alexis Martínez López
<p>

## Integrantes:

<img src="https://static.wikia.nocookie.net/houkai-star-rail/images/a/a8/Profile_Picture_Silver_Wolf_-_Opening.png/revision/latest?cb=20241023022201" alt="sw" width="200" height="200" align="right" style="margin-left: 15px;">

## Tabla de Contenidos
- [1. Introducción](#1-introducción)
- [2. Objetivos](#2-uso)
- [3. Estructura de la práctica](#3-estructura)
- [4. Explicación de la implementación](#4-implementacion)

## **1. Introducción**
### Encabezado
Esta práctica tiene como objetivo que los alumnos comprendan el concepto de reloj
en un sistema distribuido asíncrono.​
Deberán implementar dos relojes Lamport y vectorial sobre los algoritmos
desarrollados previamente.
### Desarrollo
En esta práctica se convertirá el sistema síncrono en uno parcialmente asíncrono.​
Esto se logrará introduciendo tiempos de espera aleatorios entre cada envío y
recepción de mensajes.​
Como dichos valores estarán acotados, el sistema no será completamente
asíncrono.
Para el reloj de Lamport, se utilizará como base el algoritmo de Broadcast.​
Deberán adaptar el archivo entregado en esa práctica para que cada nodo opere de forma asíncrona, y​ cuente con una variable de reloj.
Para el reloj vectorial, se tomará como base el algoritmo DFS.​
El procedimiento será el mismo que con Lamport, pero en este caso el reloj será un
arreglo de enteros.​
(Nota: será necesario modificar el constructor del nodo para indicar cuántos nodos
hay en la gráfica).

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
pytest -q test.py
```
## Pruebas pasadas:

![alt text](image.png)

## **3. Estructura**
## Estructura de la práctica

Para generarlo, en una terminal:
``` bash
tree -I 'node_modules|cache|test_*|__pycache__|.pytest_cache|venv'
```

```plaintext
      
Práctica 5 
├── Canales/                 # Sistema de comunicación entre nodos
│   ├── CanalRecorridos.py
│   └── Canal.py
├── Nodo.py                  # Clase base para todos los nodos
├── NodoBroadcast.py         # Implementación del algoritmo Broadcast
├── NodoDFS.py               # Implementaciónd el algoritmo DFS
├── NodoBFS.py               # Implementación del algortimo BFS
├── requirements.txt
├── README.md
└── test.py
```
## **4. Implementación**

### **NodoDFS**

**Atributos**:
- `padre`: Inicializado como el propio ID del nodo.
- `hijos`: Lista de nodos hijos.
- `eventos`: Lista para registrar eventos.
- `reloj`: Vector de reloj lógico (tamaño = número total de nodos).

**Método `DFS`**:
- El nodo  (id=0) inicia el algoritmo enviando un mensaje `"GO"` a su primer vecino.
- Los nodos actualizan su reloj lógico al recibir mensajes.
- Al recibir `"GO"`:
  - Establecen al emisor como su padre.
  - Si todos sus vecinos ya fueron visitados, envían `"BACK"` al padre.
  - Si hay vecinos no visitados, eligen el de menor ID y le envían `"GO"`.
- Al recibir `"BACK"`:
  - Si aún quedan vecinos no visitados, envían `"GO"` al siguiente.
  - Si no, reenvían `"BACK"` a su padre a menos que sean el nodo raiz.

---

### **NodoBFS**

**Atributos**:
- `padre`: Inicializado como el propio ID del nodo.
- `distancia`: Inicializada por math.

**Método `bfs`**:
- El nodo distinguido (id=0) inicia el algoritmo:
  - Establece su distancia en 0.
  - Envía un mensaje con `(id, distancia)` a todos sus vecinos.

Los nodos que reciben:
  - Si la distancia recibida + 1 es menor que su distancia actual:
    - Actualizan su distancia y padre.
    - Reenvían el mensaje a sus vecinos.

---

### **NodoBroadcast**

**Atributos**:
- `mensaje`: Almacena el mensaje recibido o a enviar.
- `reloj`: Reloj lógico escalar.
- `eventos`: Lista para registrar eventos.

**Método `broadcast`**:
- El nodo distinguido (id=0) inicia el envío del mensaje a todos sus vecinos.

Todos los nodos:
  - Reciben mensajes y actualizan su reloj.
  - Registran el evento de recepción.
  - Reenvían el mensaje a todos sus vecinos














