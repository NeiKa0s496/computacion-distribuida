import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoConsenso(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Consenso.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo de consenso. '''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        # Atributos extra
        self.V = [None] * (len(vecinos) + 1) # Llenamos la lista de Nodos
        self.V[id_nodo] = id_nodo
        self.New = set([id_nodo])
        self.rec_from = [None] * (len(vecinos) + 1)
        self.fallare = False      # Colocaremos esta en True si el nodo fallará
        self.lider = None         # La elección del lider.
        
        """
        Atributos adicionales para el detector de fallas:
        
        Suspectedᵢ : set
            Conjunto de IDs de procesos que este nodo sospecha que han fallado.
            Se actualiza periódicamente basado en la falta de respuesta.
            
        Crashedᵢ : list[bool]
            Lista que indica para cada proceso si se considera caído en la 
            ronda actual de detección. Se reinicia en cada ciclo del detector.
        """
        
        self.suspected = set()    # Conjunto de procesos sque se sospecha que han fallado
        self.crashed = [True] * (len(vecinos) + 1)  # LOs procesos caídos en la ronda actual
        self.beta = 2             # Intervalo para enviar INQUIRY
        self.delta = 1            # Timeout para el timer


    def consenso(self, env, f):
        '''El algoritmo de consenso.'''
        # Aquí va su implementación
        
        # Determina los nodos que fallarán
        if self.id_nodo < f:
            self.fallare = True
            return
        
        ronda = 0
        valor = self.id_nodo  # Valor inicial 
        valores_recibidos = set([valor])
        n_rondas = f + 1

        for ronda in range(n_rondas):
            """
            Esto lo cambiaré para el detector de fallas
            - Si el nodo falla en esta ronda o después, no participa
            """
            if self.id_nodo in self.suspected:
                break

            # Mensaje (id del nodo, valor propuesto, número de ronda)
            if self.New:
                # Solo enviamos a los vecinos que no son sospechosos
                vecinos_no_sospechosos = [v for v in self.vecinos if v not in self.suspected]
                if vecinos_no_sospechosos:
                    yield self.canal_salida.envia((self.id_nodo, valor, ronda), vecinos_no_sospechosos)
                    
            self.New = set()
            yield env.timeout(TICK)  # Esperar con TICK
            mensajes_ronda = []
            
            # Recibe mensajes
            while len(self.canal_entrada.items) > 0:
                    mensaje = yield self.canal_entrada.get()
                    if isinstance(mensaje, tuple) and len(mensaje) == 3:
                        id_remitente, valor_remitente, ronda_mensaje = mensaje
                        if ronda_mensaje == ronda and id_remitente not in self.suspected:
                            mensajes_ronda.append(valor_remitente)
                            self.V[id_remitente] = id_remitente
                    elif isinstance(mensaje, tuple) and len(mensaje) == 2:
                        # Mensaje del detector de fallas
                        tipo, id_emisor = mensaje
                        if tipo == "INQUIRY":
                            # Si no es sospechoso
                            if self.id_nodo not in self.suspected:
                                yield self.canal_salida.envia(("ECHO", self.id_nodo), [id_emisor])
                        elif tipo == "ECHO":
                            #proceso no está caído
                            self.crashed[id_emisor] = False
            yield env.timeout(0.01)

            # Actualiza los valores recibidos
            valores_recibidos.update(mensajes_ronda)

            # El valor propuesto es el mínimo recibido
            valor = min(valores_recibidos)
            ronda += 1

        # Cuando termina elige el líder si no es sospechoso
        if self.id_nodo not in self.suspected:
            valores_validos = [item for item in self.V if item is not None and item not in self.suspected]
            if valores_validos:
                self.lider = min(valores_validos)
        
        # Imprime el conjunto suspected al finalizar
        print(f"Nodo {self.id_nodo}: suspected = {self.suspected}, lider = {self.lider}")

    def detector_fallas(self, env, f):
        '''Implementación del detector de fallas.'''
        while True:
            # Repite cada beta time units
            for _ in range(self.beta):
                # Envia INQUIRY a todos los vecinos no sospechosos
                vecinos_no_sospechosos = [v for v in self.vecinos if v not in self.suspected]
                if vecinos_no_sospechosos and self.id_nodo not in self.suspected:
                    yield self.canal_salida.envia(("INQUIRY", self.id_nodo), vecinos_no_sospechosos)
                
                # Reinicia la lista crashed
                self.crashed = [True] * (len(self.vecinos) + 1)
                
                # Configura timer
                timer = env.timeout(self.delta)
                
                try:
                    yield timer
                except simpy.Interrupt:
                    pass
                
                # Cuando el timer expira, actualiza suspected
                self.suspected = {x for x in range(len(self.crashed)) if self.crashed[x] and x != self.id_nodo}
                
                # Si el nodo debe fallar, sale del detector
                if self.fallare:
                    return