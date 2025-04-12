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

def crearCaminoAleatorio(tamaño):
    matriz=crearMatrizNula(tamaño, tamaño)
    posX= random.randint(0, tamaño-1)
    posY= random.randint(0, tamaño-1)
    posX=0
    posY=2
    limite = determinarTotalEspacios(tamaño)
     
    while limite!=0:
    #posX>0 and posY>0 and posX<tamaño and posY<tamaño
        if matriz[posX][posY]==0:
            matriz[posX][posY]=1
            limite -= 1
        aux= random.randint(0, 3)
        if aux==0 and comprobarPosicionValida(tamaño, posX-1, posY):
            posX-=1     
        elif aux==1 and comprobarPosicionValida(tamaño, posX+1, posY):
            posX+=1
        elif aux==2 and comprobarPosicionValida(tamaño, posX, posY+1):
            posY+=1
        elif aux==3 and comprobarPosicionValida(tamaño, posX, posY-1):
            posY-=1
    return matriz
        
def determinarTotalEspacios(tamaño):
    if tamaño ==5:
        limite= random.randint(10, 15)
    elif tamaño ==10:
        limite= random.randint(40, 60)
    elif tamaño ==15:
        limite= random.randint(160, 180)
    else:
        limite= random.randint(320, 340)
    return limite

def comprobarPosicionValida(tamaño, x, y):
    if x>=0 and y>=0 and x<tamaño and y<tamaño:
        return True
    return False