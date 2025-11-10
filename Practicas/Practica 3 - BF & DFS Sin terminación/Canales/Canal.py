import simpy

class Canal():
    '''
    Interfaz que modela el comportamiento que cualquier canal debe tomar.
    '''
    def __init__(self, env: simpy.Environment, capacidad):
        '''Constructor de la clase. Se debe inicializar la lista de objetos Store al
        ser creado un canal.
        '''
        self.env = env
        self.capacidad = capacidad
        self.canales = []

    def envia(self, mensaje, vecinos):
        '''
        Envia un mensaje a los canales de entrada de los vecinos.
        '''
        if not self.canales:
            raise RuntimeError('No hay canales de entrada configurados.')
        
        eventos = []
        for indice in vecinos:
            if indice < len(self.canales):
                eventos.append(self.canales[indice].put(mensaje))
        
        return self.env.all_of(eventos) if eventos else self.env.event()


    def crea_canal_de_entrada(self):
        '''
        Creamos un objeto Store en el un nodo recibirá los mensajes.
        '''
        nuevo_canal = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(nuevo_canal)
        return nuevo_canal
