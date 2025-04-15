import csv
import flet as ft
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pathlib import Path
import Laberintos
import time

dimension = "5x5"

def setDimension(tamano):
    global dimension
    dimension = tamano

def guardarMatriz(matriz, ruta):

    if not ruta.endswith(".csv"):
        ruta+=".csv"
    try:
        file=open(ruta, "w", newline="")
        writer=csv.writer(file, delimiter=";")
        writer.writerows(matriz)
        file.close()
    except Exception as e:
        return e

def cargarMatriz(ruta):
    global matriz, dimension
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
        file.close()
    except Exception as e:
        return e

def pantalla_laberinto(page: ft.Page):
    page.window.maximized = True
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    archivo = ft.Text()
    
    
    global matriz, lista_soluciones, tiene_inicio, tiene_final, dimension, inicio, final, modoActual, documentos
    tiene_inicio = False
    tiene_final = False
    matriz = []
    lista_soluciones = []
    inicio = [0, 0]
    final = [1, 1]
    modoActual = ""
    documentos = Path.home() / "Documents"
    
    listView_soluciones = ft.ListView(
        spacing=5,
        padding=5,
        width=200,
        height=750,
        auto_scroll=False
    )

    seleccion_actual = [None]

    def clickImagen(e, x, y):
        global tiene_inicio, tiene_final
        if matriz[x][y] == 1:
            if tiene_inicio != True:
                matriz[x][y] = 2
                tiene_inicio = True
                actualizarTabla(e, False)
            elif tiene_final != True:
                matriz[x][y] = 3
                tiene_final = True
                actualizarTabla(e, False)
    
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
    matriz = Laberintos.crearCaminoAleatorio(int(dimension.split("x")[0]))
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
        global matriz, lista_soluciones
        if seleccion_actual[0] and seleccion_actual[0] != e.control:
            seleccion_actual[0].bgcolor = ft.Colors.with_opacity(0.5, '#182C61')
            seleccion_actual[0].update()

        e.control.bgcolor = ft.Colors.with_opacity(1, '#182C61')
        seleccion_actual[0] = e.control
        e.control.update()
        matriz = lista_soluciones[e.control.data]
        actualizarTabla(e, False)

    def resolverLaberinto(e):
        global matriz, lista_soluciones, tiene_inicio, tiene_final
        if tiene_inicio == False or tiene_final == False:
            
            dialogo_error = ft.AlertDialog(
                modal=True,
                title=ft.Row([
                    ft.Icon(name=ft.icons.ERROR, color=ft.Colors.RED),
                    ft.Text("Error"),
                ], spacing=10),
                content=ft.Text("Debe seleccionar un punto de inicio y fin."),
                actions_alignment=ft.MainAxisAlignment.END,
            )
            def cerrar(e):
                dialogo_error.open = False
                page.update()

            dialogo_error.actions =[ft.TextButton("Aceptar", on_click=cerrar)]
            page.overlay.append(dialogo_error)
            dialogo_error.open = True
            page.update()

        else:
            lista_soluciones = Laberintos.solucionarLaberinto(matriz, inicio[0], inicio[1], final[0], final[1])
            matriz = Laberintos.solucionOptima(lista_soluciones)

            index = lista_soluciones.index(matriz)
            if index != 0:
                temp = lista_soluciones[index]
                lista_soluciones[index] = lista_soluciones[0]
                lista_soluciones[0] = temp

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

            for paso in Laberintos.obtenerPasos(matriz):
                img = tabla_controls.controls[paso[0]].controls[1].controls[paso[1]]
                img.content.src = "camino_recorrido.jpg"
                page.update()
                time.sleep(0.3)
            

            #if not isinstance(matriz, int):
            #    actualizarTabla(e, False)

    def confirmarVolver(e):   
        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        def volver(e):
            dlg_modal.open = False
            page.update()
            page.go('/dimensiones')
        
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Salir del laberinto"),
            content=ft.Text("¿Desea salir del laberinto?"),
            actions=[
                ft.TextButton("Sí", on_click=volver),
                ft.TextButton("No", on_click=close_dlg),
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

    return ft.View(
        route="/laberinto",
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

    