import csv
import flet as ft
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pathlib import Path
import Laberintos
import time
import copy

dimension = "5x5"
mostrarMensajesError1 = True
pasos = []

def setDimension(tamano):
    global dimension
    dimension = tamano

def desactivarMensajesError(e, codigo):
    global mostrarMensajesError1
    if codigo == 1:
        mostrarMensajesError1 = False
    snackbar = ft.SnackBar(
        content=ft.Text(
            "De acuerdo, no se mostrará más el mensaje.",
            color=ft.Colors.WHITE, 
            font_family='Jersey 25', 
            size=20
        ),
        duration=2000,
        bgcolor=ft.Colors.BLACK
    )
    e.control.page.overlay.append(snackbar)
    snackbar.open = True
    e.control.page.update()


def guardarMatriz(matriz, ruta):
    if not ruta.endswith(".csv"):
        ruta+=".csv"
    try:
        file=open(ruta, "w", newline="")
        writer=csv.writer(file, delimiter=";")
        writer.writerows(Laberintos.limpiar(matriz))
        file.close()
    except Exception as e:
        return e

def cargarMatriz(ruta):
    global matriz, dimension, matriz_jugable
    try:
        file=open(ruta, "r")
        reader=csv.reader(file, delimiter=";")
        matriz = []
        temp=[]
        for row in reader:
            for i in row:
                temp+= [int(i)]
            matriz+=[temp]
            temp=[]
        matriz_jugable = copy.deepcopy(matriz)
        file.close()
    except Exception as e:
        return e

def pantalla_laberinto(page: ft.Page, modo):
    page.window.maximized = True
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    archivo = ft.Text()
    
    
    global matriz, matriz_jugable, lista_soluciones, tiene_inicio, tiene_final, dimension, inicio, final, modoActual, documentos, posicion_jugador, pasos
    tiene_inicio = False
    tiene_final = True
    matriz = []
    matriz_jugable = []
    lista_soluciones = []
    inicio = [0, 0]
    final = [1, 1]
    posicion_jugador = None
    modoActual = ""
    documentos = Path.home() / "Documents/Soluciones/"

    if not documentos.exists():
        documentos.mkdir(parents=True)
    listView_soluciones = ft.ListView(
        spacing=5,
        padding=5,
        width=200,
        height=750,
        auto_scroll=False
    )

    seleccion_actual = [None]

    def clickImagen(e, x, y):
        global tiene_inicio, tiene_final, matriz_jugable, matriz
        if matriz[x][y] == 1:
            matriz = Laberintos.limpiar(matriz)
            if tiene_inicio == True:
                if modo == "manual":
                    for i in range(len(matriz)):
                        for j in range(len(matriz[0])):
                            if matriz[i][j] == 2:
                                matriz[i][j] = 1
                                break
            if (tiene_inicio != True and modo != "manual") or modo == "manual":
                matriz[x][y] = 2
                tiene_inicio = True
                actualizarTabla(e, False)
                #elif tiene_final != True:
                    #   matriz[x][y] = 3
                    #   tiene_final = True

                #actualizarTabla(e, False)
    
    def eventoClickImagen(e):
        x, y = e.control.data
        clickImagen(e, x, y)

    def generarTabla(matriz):
        global inicio, final
        tabla = []
        cont_i = 0
        cont_j = 0
        for fila in matriz:
            items = []
            for i in fila:
                img = "bosque1.jpg"
                if i == 1 or i == 5:
                    img = "camino1.jpg"
                elif i == 2:
                    img = "inicio.jpg"
                    inicio = [cont_i, cont_j]
                elif i == 3:
                    img = "final.jpg"
                    final = [cont_i, cont_j]
                elif i == 4:
                    img = "camino_recorrido.jpg"

                w = 32
                h = 32
                if len(matriz) == 5:
                    w = 65
                    h = 65
                elif len(matriz) == 10:
                    w = 50
                    h = 50
                elif len(matriz) == 15:
                    w = 45
                    h = 45
                elif len(matriz) == 20:
                    w = 40
                    h = 40
                imagen = ft.Image(
                        src=img,
                        width=w,
                        height=h,
                        fit=ft.ImageFit.FILL
                    )
                imagen = ft.GestureDetector(
                    content=imagen,
                    on_tap=eventoClickImagen
                )
                imagen.data = (cont_i, cont_j)
                items.append(imagen)
                cont_j += 1
            
            column = ft.Column(spacing=0, controls=items)
            tabla.append(ft.Column([ ft.Text(""), column]))
            cont_i += 1
            cont_j = 0
        return tabla

    #selectorDimensiones.value = "5x5"
    if modo == "manual":
        temp= 0
    else:
        temp = 1
    matriz = Laberintos.crearCaminosAleatorios(int(dimension.split("x")[0]), temp)
    tabla_controls = ft.Row(
        controls=generarTabla(matriz),
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER
    )

    def on_file_result(e: ft.FilePickerResultEvent):
        global modoActual
        if modoActual=="guardar":
            if e.path:
                guardarMatriz(matriz, e.path)
        else:
            if e.files:
                if e.files[0].path:
                    cargarMatriz(e.files[0].path)
                    print(matriz)
                    global dimension
                    dimension = str(len(matriz)) + "x" + str(len(matriz))
                    tabla_controls.controls = generarTabla(matriz)
                    page.update()
                else:
                    archivo.value = "No se seleccionó ningún archivo."
                

    file_picker.on_result = on_file_result

    def actualizarTabla(e, generar=True):
        global matriz
        if generar:
            global tiene_inicio, tiene_final
            matriz = Laberintos.crearCaminoAleatorio(int(dimension.split("x")[0]))
            tiene_inicio = False
            tiene_final = False
        tabla_controls.controls = generarTabla(matriz)
        page.update()

    def on_click_solucion(e):
        global matriz, lista_soluciones, pasos
        pasos = []
        if seleccion_actual[0] and seleccion_actual[0] != e.control:
            seleccion_actual[0].bgcolor = ft.Colors.with_opacity(0.5, '#182C61')
            seleccion_actual[0].update()

        e.control.bgcolor = ft.Colors.with_opacity(1, '#182C61')
        seleccion_actual[0] = e.control
        e.control.update()
        matriz = lista_soluciones[e.control.data]
        actualizarTabla(e, False)

    def resolverLaberinto(e):
        global matriz, lista_soluciones, tiene_inicio, tiene_final, pasos
        if tiene_inicio == False or tiene_final == False:
            
            dialogo_error = ft.AlertDialog(
                modal=True,
                title=ft.Row([
                    ft.Icon(name=ft.icons.ERROR, color=ft.Colors.RED),
                    ft.Text("Error", font_family='Jersey 25', size=26),
                ], spacing=10),
                content=ft.Text("Debe seleccionar un punto de inicio.", font_family='Jersey 25', size=18),
                actions_alignment=ft.MainAxisAlignment.END
            )
            def cerrar(e):
                dialogo_error.open = False
                page.update()

            dialogo_error.actions =[ft.TextButton("Aceptar", style=ft.ButtonStyle(text_style=ft.TextStyle(font_family='Jersey 25', size=18)), on_click=cerrar)]
            page.overlay.append(dialogo_error)
            dialogo_error.open = True
            page.update()

        else:
            lista_soluciones = Laberintos.solucionarLaberinto(matriz)
            if lista_soluciones == -1:
                return "ERROR"
            matriz = Laberintos.solucionOptima(lista_soluciones)

            index = lista_soluciones.index(matriz)
            lista_soluciones = Laberintos.ordenarSoluciones(lista_soluciones)
            pasos = Laberintos.getTotalPasos()[index]
            #if index != 0:
            #    temp = lista_soluciones[index]
            #    lista_soluciones[index] = lista_soluciones[0]
            #    lista_soluciones[0] = temp

            for i in range(len(lista_soluciones)):
                icono = ft.Icons.CHECK
                texto = f"Solución {i+1}"
                if i == 0:
                    icono = ft.Icons.STAR
                    texto = "Mejor solución"
                item = ft.Container(
                    content=ft.Row([
                        ft.Icon(icono, ft.Colors.WHITE),
                        ft.Text(texto, size=16, color=ft.Colors.WHITE, font_family='Jersey 25'),
                        ft.Text(f"({Laberintos.cantCuatros(lista_soluciones[i])})", size=16, color=ft.Colors.GREY, font_family='Jersey 25')
                    ]),
                    bgcolor=ft.Colors.with_opacity(0.5, '#182C61'),
                    border_radius=10,
                    padding=10,
                    data=i,
                    on_click=on_click_solucion
                )
                listView_soluciones.controls.append(item)
            seleccion_actual[0] = listView_soluciones.controls[0]
            seleccion_actual[0].bgcolor = ft.Colors.with_opacity(1, '#182C61')
            listView_soluciones.update()
            recorridos = []
            for paso in pasos:#Laberintos.obtenerPasos(matriz):
                if pasos == []:
                    break
                img = tabla_controls.controls[paso[0]].controls[1].controls[paso[1]]
                antimg = None
                if pasos.index(paso) != 0:
                    antimg = tabla_controls.controls[recorridos[pasos.index(paso)-1][0]].controls[1].controls[recorridos[pasos.index(paso)-1][1]]
                #if paso in recorridos:
                #    img.content.src = "camino1.jpg"
                #else:
                if antimg != None:
                    antimg.content.src = "camino_recorrido.jpg"
                img.content.src = "jugador.jpg"
                recorridos.append(paso)
                page.update()
                time.sleep(0.3)
            actualizarTabla(e, False)

            #if not isinstance(matriz, int):
            #    actualizarTabla(e, False)

    def confirmarVolver(e):   
        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        def volver(e):
            dlg_modal.open = False
            page.on_keyboard_event = None
            page.update()
            page.go('/dimensiones')
        
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Salir del laberinto", font_family='Jersey 25', size=26),
            content=ft.Text("¿Desea salir del laberinto?", font_family='Jersey 25', size=18),
            actions=[
                ft.TextButton("Sí", on_click=volver, style=ft.ButtonStyle(text_style=ft.TextStyle(font_family='Jersey 25', size=18))),
                ft.TextButton("No", on_click=close_dlg, style=ft.ButtonStyle(text_style=ft.TextStyle(font_family='Jersey 25', size=18))),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()

    laberinto =ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(width=170),
                    ft.Container(
                        content=tabla_controls, 
                        alignment=ft.alignment.center,
                        expand=True
                    ),
                    ft.Container(content=listView_soluciones, alignment=ft.alignment.center_right)
                ],
                alignment=ft.MainAxisAlignment.START
            )
            
        ],
        scroll=ft.ScrollMode.AUTO,
    )
    
    def guardarSolucion(e):
        global modoActual
        modoActual = "guardar"
        file_picker.save_file(allowed_extensions=["csv"], initial_directory=documentos)
        
    def cargarSolucion(e):
        global modoActual
        modoActual = "cargar"
        file_picker.pick_files(initial_directory=documentos, allowed_extensions=["csv"], allow_multiple=False)

    if modo == "auto":
        tiene_inicio = True
        tiene_final = True

        matriz_jugable = copy.deepcopy(matriz)
        if mostrarMensajesError1:
            snackbar = ft.SnackBar(
                content=ft.Row(
                    controls=[
                        ft.Text("Para jugar, presione las flechas de dirección de su teclado.", color=ft.Colors.WHITE, font_family='Jersey 25', size=20),
                        ft.Container(content=ft.TextButton(
                            'No volver a mostrar', 
                            style=ft.ButtonStyle(
                                color=ft.Colors.GREY, 
                                text_style=ft.TextStyle(font_family='Jersey 25', size=20)
                            ), 
                            scale=1, 
                            on_click=lambda e: desactivarMensajesError(e, 1)), 
                            alignment=ft.alignment.bottom_right, 
                            expand=True
                        )
                    ]
                ),
                duration=4000,
                bgcolor=ft.Colors.BLACK
            )
            page.overlay.append(snackbar)
            snackbar.open = True
            page.update()

        mispasos = []

        def on_keyboard(e: ft.KeyboardEvent):
            global matriz_jugable, posicion_jugador
            #print(f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}")

            if tiene_inicio and tiene_final:
                if posicion_jugador == None:
                    posicion_jugador = inicio
                
                pos_anterior = copy.deepcopy(posicion_jugador)

                temp = 4
                if e.key == "Arrow Right":
                    if posicion_jugador[0] + 1 < len(matriz_jugable) and matriz_jugable[posicion_jugador[0]+1][posicion_jugador[1]] in [1, 2, 4]:
                        posicion_jugador[0] += 1
                    
                elif e.key == "Arrow Left":
                    if posicion_jugador[0] - 1 >= 0 and matriz_jugable[posicion_jugador[0]-1][posicion_jugador[1]] in [1, 2, 4]:
                        posicion_jugador[0] -= 1
                    
                elif e.key == "Arrow Up":
                    if posicion_jugador[1] - 1 >= 0 and matriz_jugable[posicion_jugador[0]][posicion_jugador[1]-1] in [1, 2, 4]:
                        posicion_jugador[1] -= 1

                elif e.key == "Arrow Down":
                    if posicion_jugador[1] + 1 < len(matriz_jugable[0]) and matriz_jugable[posicion_jugador[0]][posicion_jugador[1]+1] in [1, 2, 4]:
                        posicion_jugador[1] += 1

                if e.key in ["Arrow Right", "Arrow Left", "Arrow Up", "Arrow Down"]:
                    if pos_anterior != posicion_jugador:
                        imgant = tabla_controls.controls[pos_anterior[0]].controls[1].controls[pos_anterior[1]]
                        if 1==1:
                            if mispasos != [] and posicion_jugador in mispasos and imgant.content.src != "inicio.jpg":
                                imgant.content.src = "camino1.jpg"
                                if mispasos[-1] == posicion_jugador:
                                    matriz_jugable[mispasos[-1][0]][mispasos[-1][1]] = 1
                                    mispasos.pop()
                                else:
                                    index = mispasos.index(posicion_jugador)
                                    for i in range(index, len(mispasos)):
                                        img = tabla_controls.controls[mispasos[i][0]].controls[1].controls[mispasos[i][1]]
                                        if img.content.src != "inicio.jpg":
                                            img.content.src = "camino1.jpg"
                                            matriz_jugable[mispasos[i][0]][mispasos[i][1]] = 1
                                    for i in range(index, len(mispasos)):
                                        mispasos.pop()
                            else:
                                if imgant.content.src != "inicio.jpg":                 
                                    imgant.content.src = "camino_recorrido.jpg"
                                    matriz_jugable[pos_anterior[0]][pos_anterior[1]] = 4
                                    mispasos.append(pos_anterior)
                                else:
                                    mispasos.append(pos_anterior)   
                        
                        img = tabla_controls.controls[posicion_jugador[0]].controls[1].controls[posicion_jugador[1]]
                        if img.content.src != "inicio.jpg":
                            img.content.src = "jugador.jpg"
                        page.update()

        page.on_keyboard_event = on_keyboard

    return ft.View(
        route="/laberinto_" + modo,
        controls=[
            laberinto,
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.FilledButton('Volver', 
                            icon=ft.Icons.ARROW_BACK, 
                            on_click=confirmarVolver,
                            scale=3,
                            bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                            color=ft.Colors.WHITE, 
                            icon_color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                            )
                        ),
                        ft.FilledButton('Resolver', 
                            icon=ft.Icons.CHECK, 
                            on_click=resolverLaberinto,
                            scale=3,
                            bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                            color=ft.Colors.WHITE, 
                            icon_color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                            )
                        ),
                        ft.FilledButton('Guardar',
                            icon=ft.Icons.SAVE,
                            on_click=guardarSolucion,
                            scale=3, 
                            bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                            color=ft.Colors.WHITE, 
                            icon_color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                            )
                        ),
                        ft.FilledButton('Cargar',
                            icon=ft.Icons.UPLOAD_FILE_OUTLINED,
                            on_click=cargarSolucion,
                            scale=3, 
                            bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                            color=ft.Colors.WHITE, 
                            icon_color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                            )
                        )
                        
                    ],
                    spacing=250,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True
                ),
                alignment=ft.alignment.bottom_center,
                padding=50,
                expand=True,
            ),
        ],
        scroll=ft.ScrollMode.AUTO
)

    