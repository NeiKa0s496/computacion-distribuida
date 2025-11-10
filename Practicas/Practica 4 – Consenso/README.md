Practica 4: Consenso


## Profesor : Mauricio Riva Palacio Orozco
## Ayudantes:
- Adrián Felipe Fernández Romero
- Alan Alexis Martínez López
<p>

### Integrantes
<img src="sw.gif" alt="alt text" width="250" align="right" style="margin-left: 15px;">


## Tabla de Contenidos
- [1. Introducción](#1-introducción)
- [2. Uso](#2-uso)
- [3. Estructura de la práctica](#3-estructura)
- [4. Implementación](#4-implementación)

## **1. Introducción**
En esta práctica se implementará el algoritmo de consenso (sin terminación
temprana). El objetivo es comprender cómo los procesos en un sistema distribuido
pueden alcanzar un acuerdo común incluso ante fallos controlados.

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
pytest -q Test.py
```
## **3. Estructura**

```
src
├── Canales
│   ├── Canal.py
│   └── CanalRecorridos.py
├── NodoConsenso.py
├── Nodo.py
├── Practica 4.pdf
├── README.md
├── requirements.txt
└── Test.py
```

## **4. Implementación**

### Descripción General
La clase `NodoConsenso` extiende `Nodo` para implementar un algoritmo de consenso distribuido tolerante a fallos, siguiendo el algortimo de consenso distribuido sin terminación temprana.

### Comportamiento del Algoritmo

#### Inicialización
 Cada nodo propone inicialmente su propio identificador como valor propuesto
 Se configura un conjunto inicial de nodos

#### Rondas
- El algoritmo ejecuta  `f + 1` rondas de comunicación, donde `f` representa los fallos
- En cada ronda:
  - Los nodos intercambian mensajes con sus vecinos
  - Comparten y actualizan sus conjuntos de valores propuestos
  - Seleccionan el valor mínimo recibido como nuevo valor propuesto

#### Manejo de Fallos
- Algunos nodos están configurados para ser fallidos.
- Los nodos fallidos dejan de participar en el protocolo
- Continua operando correctamente con hasta `f` nodos fallidos

#### Elección del Líder
Al finalizar las rondas:
- Cada nodo selecciona como líder el primer valor válido recibido
- Todos los nodos correctos llegan al mismo acuerdo sobre la identidad del líder incluso cuando hay fallos

