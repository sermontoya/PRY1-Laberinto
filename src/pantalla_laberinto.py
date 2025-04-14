import flet as ft
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import Laberintos

dimension = "5x5"

def setDimension(tamano):
    global dimension
    dimension = tamano

def pantalla_laberinto(page: ft.Page):
    page.window.maximized = True

    global matriz, tiene_inicio, tiene_final, dimension, inicio, final
    tiene_inicio = False
    tiene_final = False
    matriz = []
    inicio = [0, 0]
    final = [1, 1]

    """
    selectorDimensiones = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("5x5"),
            ft.dropdown.Option("10x10"),
            ft.dropdown.Option("15x15"),
            ft.dropdown.Option("20x20"),
            ft.dropdown.Option("25x25"),
        ],
        text_size=16
    )
    """
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

    def actualizarTabla(e, generar=True):
        global matriz
        if generar:
            global tiene_inicio, tiene_final
            matriz = Laberintos.crearCaminoAleatorio(int(dimension.split("x")[0]))
            tiene_inicio = False
            tiene_final = False
        tabla_controls.controls = generarTabla(matriz)
        page.update()
    
    #selectorDimensiones.on_change = actualizarTabla

    def resolverLaberinto(e):
        global matriz
        matriz = Laberintos.solucionarLaberinto(matriz, inicio[0], inicio[1], final[0], final[1])
        if not isinstance(matriz, int):
            actualizarTabla(e, False)

    laberinto =ft.Column(
        controls=[
            #ft.Container(
            #    content=selectorDimensiones, 
            #    alignment=ft.alignment.top_center
            #),
            ft.Container(
                content=tabla_controls, 
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        scroll=ft.ScrollMode.AUTO,
    )

    return ft.View(
        route="/laberinto",
        controls=[
            laberinto,
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.FilledButton('Volver', 
                            icon=ft.Icons.ARROW_BACK, 
                            on_click=lambda e: page.go('/dimensiones'),
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
                        )
                    ],
                    spacing=250,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                alignment=ft.alignment.bottom_center,
                padding=50,
                expand=True
            ),
        ],
    )

    