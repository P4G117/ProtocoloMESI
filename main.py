from random import randint
import random
from procesadores import Procesador
from threading import Thread, Lock
import threading
import time
import interfaz
import  interfaz 
import tkinter as tk
import tkinter as tk
from tkinter import ttk
from tkinter import *

#Variable Global para Iniciar/Detener Flujo
global Inicia
Inicia = False

global instImprime 
instImprime = []
#Listas para los Datos
visualizarDatosMem = []
visualizarDatosBus = []
visualizarInsActual = []
visualizarInsAnteriores = []
global instAnteriores
instAnteriores = [" "," "," "," "]

#Iniciamos Flujo
def iniciaFlujo():
    global Inicia
    Inicia = True
    print("Comienzo Flujo")

#Detenemos Flujo
def detieneFlujo():
    global Inicia
    Inicia = False
    print("Detiene el Flujo")

#Funcion para la INterfaz
def creacionVenPrincipal(memoria, busControl):
    #Ventana Principal
    principal = tk.Tk()
    principal.title("Proyecto 1 - Protocolo Coherencia")
    principal.geometry('640x760')
    principal.configure(background='pink')
    #Creacion de los Canvas
    #Canvas Principal
    canvas = Canvas(principal,bg="green", width=640, height=760)
    canvas.pack()
    #Canvas para los Procesadores 
    #Procesador 1
    canvas.create_rectangle(10,30,320,160,fill="white")
    canvas.create_text(50,20,text="Procesador 1",fill="yellow")
    canvas.create_text(40,60,text="Bloque 0",fill="blue")
    canvas.create_text(40,80,text="Bloque 1",fill="blue")
    canvas.create_text(40,100,text="Bloque 2",fill="blue")
    canvas.create_text(40,120,text="Bloque 3",fill="blue")
    canvas.create_text(120,40,text="Dirección",fill="blue")
    #Direciones Bus Proce 1
    visualizarDatosBus.append(canvas.create_text(120,60,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,80,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,100,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,120,text=0,fill="black"))
    canvas.create_text(200,40,text="Dato",fill="blue")
    #Datos Bus Proce 1
    visualizarDatosBus.append(canvas.create_text(200,60,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,80,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,100,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,120,text=0,fill="black"))
    canvas.create_text(270,40,text="Estado",fill="blue")
    #Estados Bus Proce 1
    visualizarDatosBus.append(canvas.create_text(270,60,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,80,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,100,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,120,text="I",fill="black"))
    
    #Procesador 2
    canvas.create_rectangle(10,210,320,340,fill="white")
    canvas.create_text(50,200,text="Procesador 2",fill="yellow")
    canvas.create_text(40,240,text="Bloque 0",fill="blue")
    canvas.create_text(40,260,text="Bloque 1",fill="blue")
    canvas.create_text(40,280,text="Bloque 2",fill="blue")
    canvas.create_text(40,300,text="Bloque 3",fill="blue")
    canvas.create_text(120,220,text="Dirección",fill="blue")
    visualizarDatosBus.append(canvas.create_text(120,240,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,260,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,280,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,300,text=0,fill="black"))
    canvas.create_text(200,220,text="Dato",fill="blue")
    visualizarDatosBus.append(canvas.create_text(200,240,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,260,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,280,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,300,text=0,fill="black"))
    canvas.create_text(270,220,text="Estado",fill="blue")
    visualizarDatosBus.append(canvas.create_text(270,240,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,260,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,280,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,300,text="I",fill="black"))
    #Procesador 3
    canvas.create_rectangle(10,390,320,520,fill="white")
    canvas.create_text(50,380,text="Procesador 3",fill="yellow")
    canvas.create_text(40,420,text="Bloque 0",fill="blue")
    canvas.create_text(40,440,text="Bloque 1",fill="blue")
    canvas.create_text(40,460,text="Bloque 2",fill="blue")
    canvas.create_text(40,480,text="Bloque 3",fill="blue")
    canvas.create_text(120,400,text="Dirección",fill="blue")
    visualizarDatosBus.append(canvas.create_text(120,420,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,440,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,460,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,480,text=0,fill="black"))
    canvas.create_text(200,400,text="Dato",fill="blue")
    visualizarDatosBus.append(canvas.create_text(200,420,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,440,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,460,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,480,text=0,fill="black"))
    canvas.create_text(270,400,text="Estado",fill="blue")
    visualizarDatosBus.append(canvas.create_text(270,420,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,440,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,460,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,480,text="I",fill="black"))
    #Procesador 4
    canvas.create_rectangle(10,570,320,690,fill="white")
    canvas.create_text(50,560,text="Procesador 4",fill="yellow")
    canvas.create_text(40,600,text="Bloque 0",fill="blue")
    canvas.create_text(40,620,text="Bloque 1",fill="blue")
    canvas.create_text(40,640,text="Bloque 2",fill="blue")
    canvas.create_text(40,660,text="Bloque 3",fill="blue")
    canvas.create_text(120,580,text="Dirección",fill="blue")
    visualizarDatosBus.append(canvas.create_text(120,600,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,620,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,640,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(120,660,text=0,fill="black"))
    canvas.create_text(200,580,text="Dato",fill="blue")
    visualizarDatosBus.append(canvas.create_text(200,600,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,620,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,640,text=0,fill="black"))
    visualizarDatosBus.append(canvas.create_text(200,660,text=0,fill="black"))
    canvas.create_text(270,580,text="Estado",fill="blue")
    visualizarDatosBus.append(canvas.create_text(270,600,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,620,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,640,text="I",fill="black"))
    visualizarDatosBus.append(canvas.create_text(270,660,text="I",fill="black"))

    #Para Memoria 
    canvas.create_rectangle(380,210,560,400,fill="white")
    canvas.create_text(420,180,text="Memoria",font=('family=Times,weight=bold,size=14'))
    canvas.create_text(430,220,text="Dirección",fill="blue")
    canvas.create_text(430,240,text="000",fill="blue")
    canvas.create_text(430,260,text="001",fill="blue")
    canvas.create_text(430,280,text="010",fill="blue")
    canvas.create_text(430,300,text="011",fill="blue")
    canvas.create_text(430,320,text="100",fill="blue")
    canvas.create_text(430,340,text="101",fill="blue")
    canvas.create_text(430,360,text="110",fill="blue")
    canvas.create_text(430,380,text="111",fill="blue")
    canvas.create_text(500,220,text="Dato",fill="blue")
    visualizarDatosMem.append(canvas.create_text(500,240,text=0,fill="black"))
    visualizarDatosMem.append(canvas.create_text(500,260,text=0,fill="black"))
    visualizarDatosMem.append(canvas.create_text(500,280,text=0,fill="black"))
    visualizarDatosMem.append(canvas.create_text(500,300,text=0,fill="black"))
    visualizarDatosMem.append(canvas.create_text(500,320,text=0,fill="black"))
    visualizarDatosMem.append(canvas.create_text(500,340,text=0,fill="black"))
    visualizarDatosMem.append(canvas.create_text(500,360,text=0,fill="black"))
    visualizarDatosMem.append(canvas.create_text(500,380,text=0,fill="black"))
    #Instrucciones de los Procesadores
    #Procesador 1
    canvas.create_text(420,420,text="Procesador 1",font=('family=Times,weight=bold,size=14'))
    canvas.create_text(400,440,text="Inst Actual",fill="blue")
    visualizarInsActual.append(canvas.create_text(520,440,text=" ",fill="black"))
    canvas.create_text(405,460,text="Inst Anterior",fill="blue")
    visualizarInsAnteriores.append(canvas.create_text(520,460,text=" ",fill="black"))
    #Procesador 2
    canvas.create_text(420,480,text="Procesador 2",font=('family=Times,weight=bold,size=14'))
    canvas.create_text(400,500,text="Inst Actual",fill="blue")
    visualizarInsActual.append(canvas.create_text(520,500,text=" ",fill="black"))
    canvas.create_text(405,520,text="Inst Anterior",fill="blue")
    visualizarInsAnteriores.append(canvas.create_text(520,520,text=" ",fill="black"))
    #Procesador 3
    canvas.create_text(420,540,text="Procesador 3",font=('family=Times,weight=bold,size=14'))
    canvas.create_text(400,560,text="Inst Actual",fill="blue")
    visualizarInsActual.append(canvas.create_text(520,560,text=" ",fill="black"))
    canvas.create_text(405,580,text="Inst Anterior",fill="blue")
    visualizarInsAnteriores.append(canvas.create_text(520,580,text=" ",fill="black"))
    #Procesador 4
    canvas.create_text(420,600,text="Procesador 4",font=('family=Times,weight=bold,size=14'))
    canvas.create_text(400,620,text="Inst Actual",fill="blue")
    visualizarInsActual.append(canvas.create_text(520,620,text=" ",fill="black"))
    canvas.create_text(405,640,text="Inst Anterior",fill="blue")
    visualizarInsAnteriores.append(canvas.create_text(520,640,text=" ",fill="black"))
    #Creamos los Botones para Comenzar y Pausar
    btn = Button(canvas, text='Comenzar', width=5,
             height=1, bd='1' ,command=iniciaFlujo)
    btn.place(x=400, y=10)

    btn2 = Button(canvas, text='Pausar', width=10,
             height=1, bd='1',command=detieneFlujo)
    btn2.place(x=480, y=10)
    
    return principal, canvas

#Actualizamos los Datos del Bus 
def updateDatosBus(canvas,busControl):
    #Datos del Procesador 1
    canvas.itemconfigure(visualizarDatosBus[0],text = bin(busControl[0][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[1],text = bin(busControl[1][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[2],text = bin(busControl[2][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[3],text = bin(busControl[3][0])[2:].zfill(3))

    canvas.itemconfigure(visualizarDatosBus[4],text = busControl[0][1])
    canvas.itemconfigure(visualizarDatosBus[5],text = busControl[1][1])
    canvas.itemconfigure(visualizarDatosBus[6],text = busControl[2][1])
    canvas.itemconfigure(visualizarDatosBus[7],text = busControl[3][1])

    canvas.itemconfigure(visualizarDatosBus[8],text = busControl[0][2])
    canvas.itemconfigure(visualizarDatosBus[9],text = busControl[1][2])
    canvas.itemconfigure(visualizarDatosBus[10],text = busControl[2][2])
    canvas.itemconfigure(visualizarDatosBus[11],text = busControl[3][2])
    #Datos del Procesador 2
    canvas.itemconfigure(visualizarDatosBus[12],text = bin(busControl[4][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[13],text = bin(busControl[5][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[14],text = bin(busControl[6][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[15],text = bin(busControl[7][0])[2:].zfill(3))

    canvas.itemconfigure(visualizarDatosBus[16],text = busControl[4][1])
    canvas.itemconfigure(visualizarDatosBus[17],text = busControl[5][1])
    canvas.itemconfigure(visualizarDatosBus[18],text = busControl[6][1])
    canvas.itemconfigure(visualizarDatosBus[19],text = busControl[7][1])

    canvas.itemconfigure(visualizarDatosBus[20],text = busControl[4][2])
    canvas.itemconfigure(visualizarDatosBus[21],text = busControl[5][2])
    canvas.itemconfigure(visualizarDatosBus[22],text = busControl[6][2])
    canvas.itemconfigure(visualizarDatosBus[23],text = busControl[7][2])
    #Datos del Procesador 3
    canvas.itemconfigure(visualizarDatosBus[24],text = bin(busControl[8][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[25],text = bin(busControl[9][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[26],text = bin(busControl[10][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[27],text = bin(busControl[11][0])[2:].zfill(3))

    canvas.itemconfigure(visualizarDatosBus[28],text = busControl[8][1])
    canvas.itemconfigure(visualizarDatosBus[29],text = busControl[9][1])
    canvas.itemconfigure(visualizarDatosBus[30],text = busControl[10][1])
    canvas.itemconfigure(visualizarDatosBus[31],text = busControl[11][1])

    canvas.itemconfigure(visualizarDatosBus[32],text = busControl[8][2])
    canvas.itemconfigure(visualizarDatosBus[33],text = busControl[9][2])
    canvas.itemconfigure(visualizarDatosBus[34],text = busControl[10][2])
    canvas.itemconfigure(visualizarDatosBus[35],text = busControl[11][2])
    #Datos del Procesador 4
    canvas.itemconfigure(visualizarDatosBus[36],text = bin(busControl[12][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[37],text = bin(busControl[13][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[38],text = bin(busControl[14][0])[2:].zfill(3))
    canvas.itemconfigure(visualizarDatosBus[39],text = bin(busControl[15][0])[2:].zfill(3))

    canvas.itemconfigure(visualizarDatosBus[40],text = busControl[11][1])
    canvas.itemconfigure(visualizarDatosBus[41],text = busControl[12][1])
    canvas.itemconfigure(visualizarDatosBus[42],text = busControl[14][1])
    canvas.itemconfigure(visualizarDatosBus[43],text = busControl[15][1])

    canvas.itemconfigure(visualizarDatosBus[44],text = busControl[12][2])
    canvas.itemconfigure(visualizarDatosBus[45],text = busControl[13][2])
    canvas.itemconfigure(visualizarDatosBus[46],text = busControl[14][2])
    canvas.itemconfigure(visualizarDatosBus[47],text = busControl[15][2])

#Actualizamos los Datos de la Memoria 
def updateDatosMem(canvas, memoria):
        canvas.itemconfigure(visualizarDatosMem[0],text = memoria[0])
        canvas.itemconfigure(visualizarDatosMem[1],text = memoria[1])
        canvas.itemconfigure(visualizarDatosMem[2],text = memoria[2])
        canvas.itemconfigure(visualizarDatosMem[3],text = memoria[3])
        canvas.itemconfigure(visualizarDatosMem[4],text = memoria[4])
        canvas.itemconfigure(visualizarDatosMem[5],text = memoria[5])
        canvas.itemconfigure(visualizarDatosMem[6],text = memoria[6])
        canvas.itemconfigure(visualizarDatosMem[7],text = memoria[7])

#Actualizamos las Instrucciones Actuales
def updateInsActual(canvas, memoria):
        canvas.itemconfigure(visualizarInsActual[0],text = instImprime[0])
        canvas.itemconfigure(visualizarInsActual[1],text = instImprime[1])
        canvas.itemconfigure(visualizarInsActual[2],text = instImprime[2])
        canvas.itemconfigure(visualizarInsActual[3],text = instImprime[3])

#Actualizamos las Instrucciones Anteriores
def updateInsAnterior(canvas, lista):
        canvas.itemconfigure(visualizarInsAnteriores[0],text = instAnteriores[0])
        canvas.itemconfigure(visualizarInsAnteriores[1],text = instAnteriores[1])
        canvas.itemconfigure(visualizarInsAnteriores[2],text = instAnteriores[2])
        canvas.itemconfigure(visualizarInsAnteriores[3],text = instAnteriores[3])
          
#Funcion para Imprimir la Memoria
def imprimirMem(memoria):
    for i in range(8):
        print(memoria[i])

#Creamos un Procesador
def crearProces(numProce, memoria, busControl, mutex,instImprime):
    procesador = Procesador(numProce,memoria,busControl,mutex,instImprime)
    procesador.llamarProtocolo(numProce)
    time.sleep(5)

#Creamos el Hilo para cada Procesador Creado
def crearHilosProce(memoria, busControl, mutex,instImprime):
    threading.Thread(target=crearProces,args=(0, memoria,busControl,mutex,instImprime),daemon=True).start()
    time.sleep(5)
    threading.Thread(target=crearProces,args=(1, memoria,busControl,mutex,instImprime),daemon=True).start()
    time.sleep(5)
    threading.Thread(target=crearProces,args=(2, memoria,busControl,mutex,instImprime),daemon=True).start()
    time.sleep(5)
    threading.Thread(target=crearProces,args=(3, memoria,busControl,mutex,instImprime),daemon=True).start()
    time.sleep(5)

#Funcion Principal   
def main():    
    mutex = Lock()
    #Por cada Proce tengo: Dir, Dato y Estado
    #Para P1: del 0-3, bloques de la Cache 
    #Para P2: del 4-7, bloques de la Cache 
    #Para P3: del 8-11, bloques de la Cache 
    #Para P4: del 12-15, bloques de la Cache 
    busControl = [[0,0,"M"],[0,0,"I"],[6,"aabb","E"],[0,0,"I"],[6,"xyz1","I"],[0,0,"I"],[0,0,"I"],[0,0,"I"],
    [0,0,"I"],[4,0,"S"],[0,0,"I"],[0,0,"I"],[0,0,"I"],[0,0,"I"],[4,0,"S"],[0,0,"I"]]

    #Memoria Principal 
    memoria = []
    #Iniciamos/Llenamos la Memoria con Valores en Hexadecimal
    for i in range(8):
        rand_hex_str = hex(randint(15, 65535))
        memoria.append(rand_hex_str.replace("0x",""))

    #Creamos la Ventana del Programa
    window = creacionVenPrincipal(memoria, busControl)

    #Comenzamos la Ejecucion
    while(True):
        window[0].update()
        if(Inicia):      
            #Creamos lo Hilos
            crearHilosProce(memoria,busControl,mutex,instImprime)
            #Actualizamos los Datos de la MEM en la Interfaz 
            updateDatosMem(window[1],memoria)
            #Actualizamos los Datos de los Bloques en la Interfaz
            updateDatosBus(window[1],busControl)
            #Actualizamos Inst Actuales en la Interfaz
            updateInsActual(window[1],instImprime)
            #Actualizamos Insen la Interfaz
            updateInsAnterior(window[1],instAnteriores)
            #Pasamos las Inst Anteriores
            for i in range(4):
                instAnteriores[i] = instImprime[i]
            #Seteamos para las nuevas Inst
            for i in range(len(instImprime)):
                instImprime.pop(0)
            
#Iniciamos con el Protocolo y la Interfaz
main()
