#Clase para los bloques de cache 

class bloqueCache:
    #Inicializacion de la clase
    #Número del Bloque: numbloque
    #Estado del Bloque: estado
    #Dirección Memoria: direccion
    #Dato del Bloque: dato
    def __init__(self, numbloque, estado, direccion, dato):
        self.numbloque = numbloque
        self.estado = estado
        self.direccion = direccion
        self.dato = dato

    #Funciones Get
    #Para el número de Bloque 
    def getnumBloque(self):
        return self.numbloque
    #Para el número de Bloque 
    def getEstado(self):
        return self.estado
    #Para el número de Bloque 
    def getDireccion(self):
        return self.direccion
    #Para el número de Bloque 
    def getDato(self):
        return self.dato

    #Funciones Set
    #Para el número de Bloque 
    def setEstado(self, nuevo_estado):
        self.estado = nuevo_estado
    #Para el número de Bloque 
    def setDireccion(self, nueva_dir):
        self.direccion = nueva_dir
    #Para el número de Bloque 
    def setDato(self, nuevo_dato):
        self.dato = nuevo_dato

#Inicializacion de las Caches para cada Procesador
class cacheProcesador:
    def __init__(self):
        self.bloque0 = bloqueCache(0, "I", 0, 0)
        self.bloque1 = bloqueCache(1, "I", 0, 0)
        self.bloque2 = bloqueCache(2, "I", 0, 0)
        self.bloque3 = bloqueCache(3, "I", 0, 0)

