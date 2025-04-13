import random
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
    matriz=crearMatrizNula(tamano, tamano)
    limite = determinarTotalEspacios(tamano) 
    posX=0
    posY=0
    return crearCaminoAleatorio_aux(tamano, matriz, posX, posY, limite, 0)

def crearCaminoAleatorio_aux(tamano, matriz, posX, posY, limite, anterior):
    if limite==0:
        return matriz 
    if matriz[posX][posY]==0:
        matriz[posX][posY]=1
        limite -= 1
    aux= random.randint(0, 3)
    if aux==0 and comprobarPosicionValida(tamano, posX-1, posY) and comprobarAlrededores(matriz, posX-1, posY, aux):
       return crearCaminoAleatorio_aux(tamano, matriz, posX-1, posY, limite, 1)
    elif aux==1 and comprobarPosicionValida(tamano, posX+1, posY) and comprobarAlrededores(matriz, posX+1, posY, aux):  
        return crearCaminoAleatorio_aux(tamano, matriz, posX+1, posY, limite, 0)
    elif aux==2 and comprobarPosicionValida(tamano, posX, posY-1) and comprobarAlrededores(matriz, posX, posY-1, aux):
        return crearCaminoAleatorio_aux(tamano, matriz, posX, posY-1, limite, 3)
    elif aux==3 and comprobarPosicionValida(tamano, posX, posY+1) and comprobarAlrededores(matriz, posX, posY+1, aux):
        return crearCaminoAleatorio_aux(tamano, matriz, posX, posY+1, limite, 2)
    else:
    #0 que viene de izquierda, 1 que viene de derecha, 2 que viene de arriba, 3 que viene de abajo
        matriz[posX][posY]=0
        limite += 1
        if anterior==0:
            return crearCaminoAleatorio_aux(tamano, matriz, posX-1, posY, limite, 1)
        elif anterior==1:
            return crearCaminoAleatorio_aux(tamano, matriz, posX+1, posY, limite, 0)
        elif anterior==2:
            return crearCaminoAleatorio_aux(tamano, matriz, posX, posY-1, limite, 3)
        else:
            return crearCaminoAleatorio_aux(tamano, matriz, posX, posY+1, limite, 2)

def determinarTotalEspacios(tamano):
    if tamano ==5:
        limite= random.randint(10, 15)
    elif tamano ==10:
        limite= random.randint(40, 60)
    elif tamano ==15:
        limite= random.randint(160, 180)
    else:
        limite= random.randint(320, 340)
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