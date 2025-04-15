import random
import copy
def crearMatrizNula(filas, columnas):
    matriz=[]
    temp=[]
    i=0
    j=0
    while i<filas:
        while j<columnas:
            temp+=[0]
            j+=1
        matriz+=[temp]
        j=0
        i+=1
        temp=[]
    return matriz

"""def crearCaminoAleatorio(tamano):
    matriz=crearMatrizNula(tamano, tamano)
    posX= random.randint(0, tamano-1)
    posY= random.randint(0, tamano-1)
    
    limite = determinarTotalEspacios(tamano)
     
    while limite!=0:

        if matriz[posX][posY]==0 :
            matriz[posX][posY]=1
            limite -= 1
        aux= random.randint(0, 3)
        if aux==0 and comprobarPosicionValida(tamano, posX-1, posY):
            if comprobarAlrededores(matriz, posX-1, posY):
                posX-=1     
        elif aux==1 and comprobarPosicionValida(tamano, posX+1, posY):
            if comprobarAlrededores(matriz, posX+1, posY):
                posX+=1
        elif aux==2 and comprobarPosicionValida(tamano, posX, posY+1):
            if comprobarAlrededores(matriz, posX, posY+1):
                posY+=1
        elif aux==3 and comprobarPosicionValida(tamano, posX, posY-1):
            if comprobarAlrededores(matriz, posX, posY-1):
                posY-=1
    return matriz
"""
def crearCaminoAleatorio(tamano):
    
    mejorMatriz=[]
    cantUnosMejorMatriz=-1
    for i in range(10):
        matriz=crearMatrizNula(tamano, tamano)
        limite = determinarTotalEspacios(tamano) 
        matriz[0][0]=1
        aux= random.randint(0, 1)
        if aux==0:
            posX=1
            posY=0
        else:
            posX=0
            posY=1
            aux=2
        matrizTemporal=matriz 
        if crearCaminoAleatorio_aux(tamano, matrizTemporal, posX, posY, limite-1):
            return matrizTemporal
        cantidadUnos = cantUnos(matrizTemporal)
        if cantidadUnos > cantUnosMejorMatriz:
            cantUnosMejorMatriz = cantidadUnos
            mejorMatriz = matrizTemporal
    return mejorMatriz
    

def crearCaminoAleatorio_aux(tamano, matriz, posX, posY, limite):
    if limite==0:
        return True 
    if matriz[posX][posY]!=0:
        return False
    
    matriz[posX][posY]=1
    limite -= 1
    
    #0 que viene de izquierda, 1 que viene de derecha, 2 que viene de arriba, 3 que viene de abajo
    listaAux=[0, 1, 2, 3]
    random.shuffle(listaAux)
    for aux in listaAux:
        nuevaX = posX
        nuevaY= posY
        if aux == 0:
            nuevaX -= 1
        elif aux == 1:
            nuevaX += 1
        elif aux == 2:
            nuevaY -= 1
        elif aux == 3:
            nuevaY += 1
        if comprobarPosicionValida(tamano, nuevaX, nuevaY) and comprobarAlrededores(matriz, nuevaX, nuevaY, aux):
            if crearCaminoAleatorio_aux(tamano, matriz, nuevaX, nuevaY, limite):
                return True
    #matriz[posX][posY]=0
    
    return False
    """if anterior==0:
        return crearCaminoAleatorio_aux(tamano, matriz, posX-1, posY, limite, 1)
    elif anterior==1:
        return crearCaminoAleatorio_aux(tamano, matriz, posX+1, posY, limite, 0)
    elif anterior==2:
        return crearCaminoAleatorio_aux(tamano, matriz, posX, posY-1, limite, 3)
    else:
        return crearCaminoAleatorio_aux(tamano, matriz, posX, posY+1, limite, 2)"""

def determinarTotalEspacios(tamano):
    if tamano ==5:
        limite= random.randint(15, 20)
    elif tamano ==10:
        limite= random.randint(60, 75)
    elif tamano ==15:
        limite= random.randint(160, 180)
    elif tamano ==20:
        limite= random.randint(320, 340)
    else:
        limite= random.randint(540, 580)
    return limite

def comprobarPosicionValida(tamano, x, y):
    if x>=0 and y>=0 and x<tamano and y<tamano:
        return True
    return False

def comprobarAlrededores(matriz, x, y, aux):
    if aux == 0 or aux == 1:
        if comprobarPosicionValida(len(matriz), x, y-1) and matriz[x][y-1]==1:
            return False
        elif comprobarPosicionValida(len(matriz), x, y+1) and matriz[x][y+1]==1:
            return False
    elif aux == 2 or aux == 3:
        if comprobarPosicionValida(len(matriz), x-1, y) and matriz[x-1][y]==1:
            return False
        elif comprobarPosicionValida(len(matriz), x+1, y) and matriz[x+1][y]==1:
            return False
    return True

def cantUnos(matriz):
    resultado=0
    for i in matriz:
        for j in i:
            if j==1:
                resultado+=1
    return resultado

def ordenarSoluciones(soluciones):
    if len(soluciones) <= 1:
        return soluciones
    pivote = soluciones[0]
    menores = []
    mayores = []
    for i in range(1, len(soluciones)):
        solucion = soluciones[i]
        if cantCuatros(solucion) < cantCuatros(pivote):
            menores.append(solucion)
        else:
            mayores.append(solucion)
    return ordenarSoluciones(menores) + [pivote] + ordenarSoluciones(mayores)

def solucionarLaberinto(matriz, inicioX, inicioY, finX, finY):
    soluciones=[]
    cantPasosMejorMatriz=1000
    tamano=len(matriz)
    intentos=10
    if tamano==10:
        intentos=20
    elif tamano==15:
        intentos=50
    elif tamano==20:
        intentos=100
    elif tamano==25:
        intentos=150
    for i in range(intentos): 
        matrizTemporal=copy.deepcopy(matriz)
        if solucionarLaberinto_aux(tamano, matrizTemporal, inicioX, inicioY, finX, finY, inicioX, inicioY, 0, cantPasosMejorMatriz, -1):
            if matrizTemporal not in soluciones:
                soluciones+=[matrizTemporal]
    if soluciones==[]:
        return -1
    return ordenarSoluciones(soluciones)


def solucionarLaberinto_aux(tamano, matriz, inicioX, inicioY, finX, finY, posX, posY, cuatros, limite, anterior):
    if posX == finX and posY == finY:
        return True
    
    temp = matriz[posX][posY]
    
    if temp!=1 and temp!=2:
        return False
    if temp != 2 and temp != 5:
        matriz[posX][posY] = 4 
        cuatros += 1

    listaAux = [0, 1, 2, 3]
    random.shuffle(listaAux)
    for aux in listaAux:
        nuevaX = posX
        nuevaY = posY
        if aux == 0: #and anterior != 1: 
            nuevaX -= 1
        elif aux == 1: #and anterior != 0: 
            nuevaX += 1
        elif aux == 2: #and anterior != 3: 
            nuevaY -= 1
        elif aux == 3: #and anterior != 2: 
            nuevaY += 1
        if comprobarPosicionValida(tamano, nuevaX, nuevaY):
            if solucionarLaberinto_aux(tamano, matriz, inicioX, inicioY, finX, finY, nuevaX, nuevaY, cuatros, limite, aux):
                return True
    if temp != 2:
        matriz[posX][posY] = 5 
    return False

def solucionOptima(listaMatrices):
    cantPasosMejorSolucion=cantCuatros(listaMatrices[0])
    mejorSolucion=listaMatrices[0]
    for matriz in listaMatrices:
        cantPasos=cantCuatros(matriz)
        if cantPasosMejorSolucion>cantPasos:
            cantPasosMejorSolucion=cantPasos
            mejorSolucion=matriz
    return mejorSolucion
        

def cantCuatros(matriz):
    resultado=0
    for i in matriz:
        for j in i:
            if j==4:
                resultado+=1
    return resultado


"""
cantidadPasos = cantCuatros(matrizTemporal)
            print(cantidadPasos)
            if cantidadPasos < cantPasosMejorMatriz and cantidadPasos > 0:
                cantPasosMejorMatriz = cantidadPasos
                mejorSolucion = matrizTemporal
                
logica para obtener el mejor camino

"""


