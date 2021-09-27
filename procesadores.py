#Creacion de la Clase Procesador 
import scipy.stats
from scipy.stats import poisson
from random import getrandbits, randrange
from random import randint
from random import randrange
import random 
import bloqueCache
import protocolo
import time

#Variables para Probabilidad de Poisson
#mu = 0.5
k = randrange(11)

#Generacion de la Direccion para la Instruccion: Caso Read y Write
def direccion():
    return random.randint(0,7)

#Generacion del Dato de la Instruccion: Caso del Write 
def dato():
    rand_hex_str = hex(randint(16, 65535))
    return rand_hex_str.replace("0x","") 

#Funcion para juntar en un String la Inst
def instFinal(ar):
    if(ar[1]==0):
        store = "P" + str(ar[0]) + ":" + " " + "calc"
    elif(ar[1]== 1):
        store = "P" + str(ar[0]) + ":" + " " + "read" + "," + " " + str(bin(ar[2])[2:].zfill(3)) 
    else:
        store = "P" + str(ar[0]) + ":" + " " + "write" + "," + " " + str(bin(ar[2])[2:].zfill(3)) + "," + " " + str(ar[3])
    return store

#Creacion de Cache 
#Clase del Procesador
class Procesador:
    #Inicializamos el Procesador 
    def __init__(self, numeroProce, memoria, busControl, mutex,instImprime):
        self.numProce = numeroProce
        self.memoria = memoria
        self.bus = busControl
        self.mutex = mutex
        self.cache = bloqueCache.cacheProcesador()
        self.hola = instImprime
        

    #Creacion de las Instrucciones 
    def crearInstr(self, numProce):
        #Instrucciones Posibles
        mu = random.randint(0,10)
        #Calc = 0, Read = 1, Write = 2
        inst = poisson.rvs(mu,loc=k,size=1,random_state=None)
        var = [] #NumProce, Inst, Direccion y Dato
        if(0 <= inst <=3):       
            var = [numProce, 0,0,0]
            return var
        elif(4 <= inst <=7):
            var = [numProce, 1,direccion(),0]
            return var
        else:
            var = [numProce, 2,direccion(),dato()]
            return var
    #Actualizar los Bloques de la Cache
    def actualizar(self, numProce):
        cacheActual = []
        for i in range(4):
            cacheActual.append(self.bus[numProce*4+i])

        self.cache.bloque0.setEstado(cacheActual[0][2])
        self.cache.bloque0.setDato(cacheActual[0][1])
        self.cache.bloque0.setDireccion(cacheActual[0][0])

        self.cache.bloque1.setEstado(cacheActual[1][2])
        self.cache.bloque1.setDato(cacheActual[1][1])
        self.cache.bloque1.setDireccion(cacheActual[1][0])

        self.cache.bloque2.setEstado(cacheActual[2][2])
        self.cache.bloque2.setDato(cacheActual[2][1])
        self.cache.bloque2.setDireccion(cacheActual[2][0])

        self.cache.bloque3.setEstado(cacheActual[3][2])
        self.cache.bloque3.setDato(cacheActual[3][1])
        self.cache.bloque3.setDireccion(cacheActual[3][0])
    
    #Imprimir los valores de los bloques de Cache
    def imprimirCache(self):
        
        print(self.cache.bloque0.getEstado())
        print(self.cache.bloque0.getDato())
        print(self.cache.bloque0.getDireccion())

        print(self.cache.bloque1.getEstado())
        print(self.cache.bloque1.getDato())
        print(self.cache.bloque1.getDireccion())

        print(self.cache.bloque2.getEstado())
        print(self.cache.bloque2.getDato())
        print(self.cache.bloque2.getDireccion())

        print(self.cache.bloque3.getEstado())
        print(self.cache.bloque3.getDato())
        print(self.cache.bloque3.getDireccion())

    #Funcion de Prueba
    def cambiaCache(self,pos):
        self.bus[pos][0] = random.getrandbits(10)
        self.bus[pos][1] = random.getrandbits(10)
        self.bus[pos][2] = "Haloooo"
    
    #Funcion para imprimir el Bus de Control
    def imprimirBus(self):
        for i in range(16):
            print(self.bus[i])
            print("\n")

    #Funcion para llamar al Protocolo 
    def llamarProtocolo(self,numProce):
        time.sleep(2) 
        timewait = randint(1,5)
        self.actualizar(numProce)
        inst = self.crearInstr(numProce)
        print(" ------------------ Procesador en Ejecución:", numProce, "----------------------")
        store = instFinal(inst)
        self.hola.append(store)
        print("La Instruccion es", store)
        print("---------------- Comenzamos el Protocolo MESI ---------------")
        self.mutex.acquire()
        protocolo.protoMesi(self,inst,numProce,self.memoria,self.bus,self.cache)
        self.mutex.release()
        time.sleep(timewait)
        