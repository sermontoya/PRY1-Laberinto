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
    print("Posicion inicial: ", posX, posY)
    while posX>0 and posY>0 and posX<tamaño and posY<tamaño:
        if matriz[posX][posY]==0:
            matriz[posX][posY]=1
        aux= random.randint(0, 3)
        if aux==0:
            posX-=1     
        elif aux==1:
            posX+=1
        elif aux==2:
            posY+=1
        else:
            posY-=1
    return matriz
        
    