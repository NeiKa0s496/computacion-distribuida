# Práctica 6 - Detección de Fallas en Sistemas Distribuidos

## Descripción de la práctica


Los detectores de fallas son una herramienta esencial en los sistemas distribuidos,
ya que permiten mantener la integridad del sistema cuando uno o varios procesos
dejan de responder.

<img src="https://upload-os-bbs.hoyolab.com/upload/2024/06/20/329888290/6aa7d148cf742e3b8c4432ecc5fee482_2993125988332696065.jpg?x-oss-process=image%2Fresize%2Cs_1000%2Fauto-orient%2C0%2Finterlace%2C1%2Fformat%2Cwebp%2Fquality%2Cq_70" style="float: right; margin-left: 15px; width: 300px; height: 300px; object-fit: cover;" />

En esta práctica implementarán un detector de fallas sencillo, basado en el siguiente
esquema, cuyo propósito es identificar procesos que pueden haber fallado durante
la ejecución del algoritmo.

## Descripción de la implementación del detector de fallas
Se implementó el detector de fallos según el esquema:

1. **Inicialización**: `suspected_i ← ∅`
2. **Repetir cada β unidades de tiempo**:
   - Envía mensajes INQUIRY a todos los vecinos no sospechosos (j que no esta en los suspected)
   - Reinicia la lista `crashed_i`
   - Configura un timer de Δ unidades
3. **Cuando recibe INQUIRY**: Responde con ECHO
4. **Cuando recibe ECHO**: Marca el proceso como no caído
5. **Expiración del timer**: Actualiza `suspected_i` con los procesos que no respondieron

### Modificaciones al Algoritmo de Consenso
- Los nodos solo envían mensajes a vecinos que no están en su conjunto `suspected`
- Los nodos ignoran mensajes de procesos sospechosos
- El detector se ejecuta en paralelo con el algoritmo de consenso
- Al finalizar cada nodo imprime su conjunto `suspected`

##  Preguntas

1. **¿A qué clase pertenece este detector de fallos?**

   Me parece que pertenece a la clase de detectores de fallas por timeout, específicamente un detector de fallas por ausencia de respuesta.

2. **¿Qué cambios tendrías que realizar para que el detector pudiera ejecutarse indefinidamente cada k rondas?**
   Modificaríamos el bucle principal del detector para que sea infinito y podríamos ponerle un parámetro `k` que controle la frecuencia de ejecución. También necesitaríamos mecanismos para detenerlo cuando el consenso termine.

3. **¿Tienes alguna sugerencia, queja o comentario sobre el laboratorio?**
   Me hubiera gustado que talvez fuera al menos una clase a la semana en virtual o algunas explicaciones pregrabadas, la verdad agradezco mucho que fuera de esta manera también como no tanto el el salón porque de repente tengo problemas personales que me impiden ir a la facutad asi que me resultó muy conveniente. También me hubiera gustado que talvez nos hubieran dado material para referenciarnos en cada práctica, tipo videos o algo de algún libro de antemano en el pdf.

## **Uso**
### En una terminal :
- Generamos el entorno virtual

```bash
python3 -m venv venv
```
Dentro de src/:
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
python TestPractica6.py
```
## **Estructura**
## Estructura de la práctica

Para generarlo, en una terminal:
``` bash
tree -I 'node_modules|cache|test_*|__pycache__|.pytest_cache|venv'
```

```plaintext
Práctica 6 - Detección de Fallas en Sistemas Distribuidos
├── README.md
└── src
    ├── Canales
    │   ├── Canal.py
    │   └── CanalRecorridos.py
    ├── NodoConsenso.py
    ├── Nodo.py
    ├── requirements.txt
    └── Test.py
```

<img src="https://upload-os-bbs.hoyolab.com/upload/2024/07/28/200963534/64f00a0f60391fb21951da5be882a0ee_199227901792397536.gif" alt="sw" align="center">
