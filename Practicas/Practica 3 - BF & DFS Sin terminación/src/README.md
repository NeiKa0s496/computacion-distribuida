# Practica 3: BF & DFS Sin terminación

## Profesor : Mauricio Riva Palacio Orozco
## Ayudantes:
- Adrián Felipe Fernández Romero
- Alan Alexis Martínez López
<p>

## Tabla de Contenidos
- [1. Introducción](#1-introducción)
- [2. Uso](#2-uso)
- [3. Estructura de la práctica](#3-estructura)
- [4. Explicación de la implementación](#4-implementacion)

## **1. Introducción**
En esta práctica implementamoas los algortimos dfs y bfs en sus versiones que no detectan terminacion usando de guía el pseudocódigo que se nos dío en la carpeta práctica 3.

## **2.Uso**
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
pytest Test.py
```
## **3. Estructura**
En una terminal: 
```bash
tree -I 'node_modules|cache|test_*|__pycache__|.pytest_cache|venv'
```
```
├── Canales
│   ├── Canal.py
│   └── CanalRecorridos.py
├── NodoBFS.py
├── NodoDFS.py
├── Nodo.py
├── README.md
├── requirements.txt
└── Test.py
```

## **4. Implementación**
