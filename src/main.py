import flet as ft
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import Laberintos

def main(page: ft.Page):
    page.window.maximized = True

    dd = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("5x5"),
            ft.dropdown.Option("10x10"),
            ft.dropdown.Option("15x15"),
            ft.dropdown.Option("20x20"),
            ft.dropdown.Option("25x25"),
        ],
    )
    
    def generarTabla(matriz):
        tabla = []
        for fila in matriz:
            items = []
            for i in fila:
                img = "bosque1.jpg"
                if i == 1:
                    img = "camino1.jpg"
                items.append(
                    ft.Image(
                        src=img,
                        width=40,
                        height=40,
                        fit=ft.ImageFit.FILL
                    )
                )
            column = ft.Column(spacing=0, controls=items)
            tabla.append(ft.Column([ ft.Text(""), column]))
        return tabla
    
    dd.value = "5x5"
    matriz = Laberintos.crearCaminoAleatorio(int(dd.value.split("x")[0]))
    tabla_controls = ft.Row(
        controls=generarTabla(matriz),
        spacing=0,
        alignment=ft.MainAxisAlignment.START
    )

    def actualizarTabla(e):
        matriz = Laberintos.crearCaminoAleatorio(int(dd.value.split("x")[0]))
        tabla_controls.controls = generarTabla(matriz)
        page.update()
    
    dd.on_change = actualizarTabla
    page.add(dd)
    page.add(tabla_controls)


ft.app(main, assets_dir="assets")
