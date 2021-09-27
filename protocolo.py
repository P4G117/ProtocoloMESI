#Protocolo MESI
import bloqueCache
import time 
import random 

#Funcion Principal del Protocolo de Coherencia MESI
def protoMesi(self, inst, numProce, memoria, bus, cache):
    print("Iniciamos Protcolo")
    #Caso de que la Inst es el Calc 
    if(inst[1] == 0):
        #time.sleep(1)
        print("La Instruccion fue un Calc")
        time.sleep(2)

    #Caso de que la Inst es Read
    elif(inst[1]==1):
        print("La Instruccion fue un Read")
        #Primer Caso: Read Hit
        dir = inst[2]
        #Lo encontre en mi Cache
        if((buscarCache(self,dir,cache) == True) and (diffInvalido(self,dir,cache)==True)):
            print("Caso 1: Hubo un Read Hit")
        #No lo Encontre en mi cache: Read Miss
        #Lo voy a buscar a las Otras Caches
        #Aqui buscaría en el Bus 
        #Caso 1: Read Miss - Read Hit
        else:
            print("Caso 2: Hubo un Read Miss")
            if(buscarBus(self,dir,bus)==True):
                #Lo encontre en Otra Cache
                print("Read Miss -> Read Hit en Otra Cache")
                otraCache(self,dir,bus,self.numProce)
            else:
                print("Caso 3: Hubo un Read Miss Miss")
                print("Caso 3: Leo directo de Memoria")
                #Caso 2: Read Miss - Read Miss
                #No lo encontre en ninguna Otra Cache
                #Tengo que ir hasta Memoria 
                nuevoDato = memoria[dir]
                setNuevoDatoCache(self,numProce,bus,dir,nuevoDato)
    else:
        print("La Instruccion fue un Write")
        dir = inst[2]
        #Caso 1: Write Hit en mi Cache
        #Escribo el nuevo dato en Memoria - Write Back desde mi Cache
        #Paso de E a M / Si estoy en M me quedo en M
        #Si estoy en S busco en las Otras Caches y las paso I 
        if((buscarCache(self,dir,cache) == True)):
            print("Caso 1: Write Hit")
            aux = verficaEstado(self,bus,dir)
            if(aux[0] == 1 or aux[0] == 2):
                print("Caso 1.1: Estado del Bloque es E O M")
                dato = estadoM(self,dir,cache)
                #Hariamos Write Back
                memoria[dir]= dato[0]
                #Escribimos Datos en nuestra Cache
                setNuevoDatoCache2(self, numProce,bus,dir,inst[3],dato[1])
            elif(aux[0]==3):
                print("Caso 1.2: Estado del Bloque es S")
                dato = cambioEstadoSE(self,dir,cache)
                #Hariamos Write Back
                memoria[dir] = dato[0]
                #Invalidamos a Todos los que tengan esa Direccion en S
                pasarInvalido(self,dir,bus)
                #Escribimos Datos en nuestra Cache
                setNuevoDatoCache3(self, numProce,bus,dir,inst[3],dato[1])               
            else:
                print("Caso 1.3: Estado del Bloque es I")
                dato = estadoI(self,dir,cache)
                invalidarME(self,bus,dir,memoria)
                setNuevoDatoCache3(self, numProce,bus,dir,inst[3],dato[0])
                      
        #Caso 2: Write Miss de mi Cache y Write Hit en las Otras Caches
        #Escribo el nuevo dato en Memoria - Write Back desde la Otra Cache
        #Paso de E/M a I en la Otra Cache
        #Si esta en S busco en las Otras Caches y las paso I 
        elif((buscarCache(self,dir,cache) == False ) and (buscarBus(self,dir,bus)==True)):
            aux = verficaEstado(self,bus,dir)
            print("Caso 2: Write Miss")
            if(aux[0] == 1 or aux[0] == 2):
                print("Caso 2.1: Estado del Bloque E o M en la Cache donde hubo Hit")
                self.bus[aux[1]][2]="I"
                #Hariamos Write Back
                memoria[dir]=self.bus[aux[1]][1]
                #Escribimos Datos en nuestra Cache
                setNuevoDatoCache(self, numProce,bus,dir,inst[3])
            elif(aux[0]==3):
                print("Caso 2.2: Estado del Bloque S en la Cache donde hubo Hit")
                self.bus[aux[1]][2]="I"
                #Hariamos Write Back
                memoria[dir]=self.bus[aux[1]][1]
                #Invalidamos a Todos los que tengan esa Direccion en S
                pasarInvalido(self,dir,bus)
                #Escribimos Datos en nuestra Cache
                setNuevoDatoCache(self, numProce,bus,dir,inst[3])
                
            elif(aux[0]==4):
                print("Caso 2.3: Estado del Bloque I en la Cache donde hubo Hit")
                memoria[dir]=inst[3]
                setNuevoDatoCache(self, numProce,bus,dir,inst[3])
        #Caso 3: Write Miss de mi Cache y Write Miss de las Otras Caches
        #Escribo el nuevo dato en Memoria 
        #Modifico Dir, Dato y Estado(pasa a E)
        
        elif((buscarCache(self,dir,cache) == False )and (buscarBus(self,dir,bus)==False)):
            print("Caso 3: Write Miss - Miss")
            print("Vamos directo a Memoria")
            memoria[dir]=inst[3]
            setNuevoDatoCache(self, numProce,bus,dir,memoria[dir])

#Write Hit - Estado de mi Cache = I
#Tengo que Invalidar en las Otras Caches si estan en E/M para esa Direccion
def invalidarME(self,bus,dir,memoria):
    for i in range(16):
        if(self.bus[i][0]==dir and self.bus[i][2] != "M"):
            self.bus[i][2] = "I"
            memoria[dir] = self.bus[i][1]
        if(self.bus[i][0]==dir and self.bus[i][2] != "E"):
            self.bus[i][2] = "I"
            memoria[dir] = self.bus[i][1]
            
#Write Hit - Cambio Estado de E a M 
def cambioEstadoEM(self, direccion, cache):
    dato = []
    if(direccion == self.cache.bloque0.getDireccion()):
        if(self.cache.bloque0.getEstado() == "E"):
            self.cache.bloque0.setEstado("M") 
            dato.append(self.cache.bloque0.getDato())
            dato.append(0)
            return dato
    if(direccion == self.cache.bloque1.getDireccion()):
        if(self.cache.bloque1.getEstado() == "E"):
            self.cache.bloque1.setEstado("M") 
            dato.append(self.cache.bloque1.getDato())
            dato.append(1)
            return dato
    if(direccion == self.cache.bloque2.getDireccion()):
        if(self.cache.bloque2.getEstado() == "E"):
            self.cache.bloque2.setEstado("M") 
            print(self.cache.bloque2.getEstado())
            dato.append(self.cache.bloque2.getDato())
            dato.append(2)
            return dato
    if(direccion == self.cache.bloque3.getDireccion()):
        if(self.cache.bloque3.getEstado() == "E"):
            self.cache.bloque3.setEstado("M") 
            dato.append(self.cache.bloque3.getDato())
            dato.append(3)
            return dato
    return dato

#Verifica si el Estado del Bloque es M
def estadoM(self, direccion, cache):
    dato = []
    if(direccion == self.cache.bloque0.getDireccion()):
        dato.append(self.cache.bloque0.getDato())
        dato.append(0)
        return dato
    if(direccion == self.cache.bloque1.getDireccion()):
        dato.append(self.cache.bloque1.getDato())
        dato.append(1)
        return dato
    if(direccion == self.cache.bloque2.getDireccion()):
        dato.append(self.cache.bloque2.getDato())
        dato.append(2)
        return dato
    if(direccion == self.cache.bloque3.getDireccion()):
        dato.append(self.cache.bloque3.getDato())
        dato.append(3)
        return dato

#Verifica si el Estado del Bloque es I
def estadoI(self, direccion, cache):
    dato = []
    if(direccion == self.cache.bloque0.getDireccion()):
        dato.append(0)
        return dato
    if(direccion == self.cache.bloque1.getDireccion()):
        dato.append(1)
        return dato
    if(direccion == self.cache.bloque2.getDireccion()):
        dato.append(2)
        return dato
    if(direccion == self.cache.bloque3.getDireccion()):
        dato.append(3)
        return dato

#Write Hit - Cambio el Estado del Bloque de S a E 
def cambioEstadoSE(self, direccion, cache):
    dato = []
    if(direccion == self.cache.bloque0.getDireccion()):
        if(self.cache.bloque0.getEstado() == "S"):
            self.cache.bloque0.setEstado("E") 
            dato.append(self.cache.bloque0.getDato())
            dato.append(0)
            return dato
    if(direccion == self.cache.bloque1.getDireccion()):
        if(self.cache.bloque1.getEstado() == "S"):
            self.cache.bloque1.setEstado("E") 
            dato.append(self.cache.bloque1.getDato())
            dato.append(0)
            return dato
    if(direccion == self.cache.bloque2.getDireccion()):
        if(self.cache.bloque2.getEstado() == "S"):
            self.cache.bloque2.setEstado("E")
            dato.append(self.cache.bloque2.getDato())
            dato.append(0)
            return dato
    if(direccion == self.cache.bloque3.getDireccion()):
        if(self.cache.bloque3.getEstado() == "S"):
            self.cache.bloque3.setEstado("E") 
            dato.append(self.cache.bloque3.getDato())
            dato.append(0)
            return dato

#Para Buscar en la Cache Propia a ver si hay un Hit
def buscarCache(self, direccion, cache):
    if(direccion == self.cache.bloque0.getDireccion()):
        if(self.cache.bloque0.getEstado() != "I"):
            return True
    if(direccion == self.cache.bloque1.getDireccion()):
        if(self.cache.bloque1.getEstado() != "I"):
            return True
    if(direccion == self.cache.bloque2.getDireccion()):
        if(self.cache.bloque2.getEstado() != "I"):
            return True
    if(direccion == self.cache.bloque3.getDireccion()):
        if(self.cache.bloque3.getEstado() != "I"):
            return True
    return False

#Para saber si el Estado del Bloque es diferente a Invalido
def diffInvalido(self, direccion, cache):
    if(direccion == self.cache.bloque0.getDireccion()):
        return True
    if(direccion == self.cache.bloque1.getDireccion()):
        return True
    if(direccion == self.cache.bloque2.getDireccion()):
        return True
    if(direccion == self.cache.bloque3.getDireccion()):
        return True
    return False

#Cambiamos Estado de la Otra Cache donde Encontramos el Dato para Read Miss -> Read Hit
def cambiarEstOtrCacheRM(self, bloque, bus):
    if(self.bus[bloque][2] == "M"):
        self.bus[bloque][2] = "S"
    if(self.bus[bloque][2] == "E"):
        self.bus[bloque][2] = "S"
    if(self.bus[bloque][2] == "S"):
        self.bus[bloque][2] = "S"

#Cambio Estado de la Cache desde donde Intente hacer la Instruccion 
def cambiarEstCachePropiaRM(self, numProce,bus,dir):
    #Primer Caso. Primer Bloque del Procesador
    if(self.bus[numProce*4][0]==dir):
        if(self.bus[numProce*4][2] == "S"):
            self.bus[numProce*4][2] = "S"
        if(self.bus[numProce*4][2] == "I"):
            self.bus[numProce*4][2] = "S"
        if(self.bus[numProce*4][2] == "E"):
            self.bus[numProce*4][2] = "S"
        if(self.bus[numProce*4][2] == "M"):
            self.bus[numProce*4][2] = "S"
    #Segundo Caso. Segundo Bloque del Procesador
    if(self.bus[numProce*4+1][0]==dir):
        if(self.bus[numProce*4+1][2] == "S"):
            self.bus[numProce*4+1][2] = "S"
        if(self.bus[numProce*4+1][2] == "I"):
            self.bus[numProce*4+1][2] = "S"
        if(self.bus[numProce*4+1][2] == "E"):
            self.bus[numProce*4+1][2] = "S"
        if(self.bus[numProce*4+1][2] == "M"):
            self.bus[numProce*4+1][2] = "S"
    #Tercer Caso. Tercer Bloque del Procesador
    if(self.bus[numProce*4+2][0]==dir):
        if(self.bus[numProce*4+2][2] == "S"):
            self.bus[numProce*4+2][2] = "S"
        if(self.bus[numProce*4+2][2] == "I"):
            self.bus[numProce*4+2][2] = "S"
        if(self.bus[numProce*4+2][2] == "E"):
            self.bus[numProce*4+2][2] = "S"
        if(self.bus[numProce*4+2][2] == "M"):
            self.bus[numProce*4+2][2] = "S"
    #Tercer Caso. Tercer Bloque del Procesador
    if(self.bus[numProce*4+3][0]==dir):
        if(self.bus[numProce*4+3][2] == "S"):
            self.bus[numProce*4+3][2] = "S"
        if(self.bus[numProce*4+3][2] == "I"):
            self.bus[numProce*4+3][2] = "S"
        if(self.bus[numProce*4+3][2] == "E"):
            self.bus[numProce*4+3][2] = "S"
        if(self.bus[numProce*4+3][2] == "M"):
            self.bus[numProce*4+3][2] = "S"

#Buscar si la Direccion esta en Otra Cache
def buscarBus(self,dir,bus):
    for i in range(16):
        if(self.bus[i][0]==dir):
            return True
    return False

#Obtener Bloque de la Cache del Bus donde se encontro la Dirección 
def otraCache(self, dir,bus,numProce):
    for i in range(16):
        if(self.bus[i][0]==dir and self.bus[i][2] != "I"):
            self.bus[i][2] = "S"
            setNuevoDatoCacheMH(self, numProce,bus,dir,self.bus[i][1])

#Pasamos el Estado de un Bloque de S a I
def pasarInvalido(self, dir,bus):
    for i in range(16):
        if(self.bus[i][0]==dir and self.bus[i][2] == "S"):
            self.bus[i][2] = "I"

#Verifica el Estado del Bloque para saber si es E, M, S o I
def verficaEstado(self,bus,dir):
    aux = []
    for i in range(16):
        if(self.bus[i][0]==dir):
            if(self.bus[i][2] == "M"):
                aux.append(1)
                aux.append(i)
                return aux
            if(self.bus[i][2] == "E"):
                aux.append(2)
                aux.append(i)
                return aux
            if(self.bus[i][2] == "S"):
                aux.append(3)
                aux.append(i)
                return aux
            else:
                aux.append(4)
                return aux

#Setear Nuevo Estado a la Cache desde donde Busque 
#Traemos el dato desde Memoria
def setNuevoDatoCache(self, numProce,bus,dir,dato):
    #Estariamos haciendo el Set siempre en el bloque 
    pos = random.randint(0,3)
    self.bus[numProce*4 + pos][0] = dir
    self.bus[numProce*4 + pos][1] = dato
    self.bus[numProce*4 + pos][2] = "E"

def setNuevoDatoCache2(self, numProce,bus,dir,dato,posBloque):
    #Estariamos haciendo el Set siempre en el bloque 
    pos = posBloque
    self.bus[numProce*4 + pos][0] = dir
    self.bus[numProce*4 + pos][1] = dato
    self.bus[numProce*4 + pos][2] = "M"

def setNuevoDatoCache3(self, numProce,bus,dir,dato,posBloque):
    #Estariamos haciendo el Set siempre en el bloque 
    pos = posBloque
    self.bus[numProce*4 + pos][0] = dir
    self.bus[numProce*4 + pos][1] = dato  
    self.bus[numProce*4 + pos][2] = "E"

def setNuevoDatoCacheMH(self, numProce,bus,dir,dato):
    #Estariamos haciendo el Set siempre en el bloque 
    pos = random.randint(0,3)
    self.bus[numProce*4 + pos][0] = dir
    self.bus[numProce*4 + pos][1] = dato
    self.bus[numProce*4 + pos][2] = "S"         