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

print(crearMatrizNula(5,5))