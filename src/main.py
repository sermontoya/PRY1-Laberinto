import flet as ft
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import Laberintos

def main(page: ft.Page):

    matriz = Laberintos.crearCaminoAleatorio(15)
    print(matriz)
    
    def generarTabla(matriz):
        tabla = []
        for fila in matriz:
            items = []
            for i in fila:
                color = ft.Colors.BLUE
                if i == 1:
                    color = ft.Colors.WHITE
                items.append(
                    ft.Container(
                        content=ft.Text(value=""),
                        #content=ft.Text(value=str(i)),
                        alignment=ft.alignment.center,
                        width=40,
                        height=40,
                        bgcolor=color,
                        border_radius=ft.border_radius.all(0),
                    )
                )
            column = ft.Column(spacing=0, controls=items)
            tabla.append(ft.Column([ ft.Text(""), column]))
        return tabla
    
    page.add(
        ft.Row(
            controls=generarTabla(matriz),
            spacing=0,  # Espacio entre columnas
            alignment=ft.MainAxisAlignment.START
        )
    )


ft.app(main)
