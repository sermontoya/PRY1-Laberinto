import flet as ft


def main(page: ft.Page):
    
    matriz = [
        [1, 0, 0, 0, 0],
        [1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 1, 1],
    ]
    
    def generarTabla(matriz):
        tabla = []
        for fila in matriz:
            items = []
            for i in fila:
                items.append(
                    ft.Container(
                        content=ft.Text(value=str(i)),
                        alignment=ft.alignment.center,
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.BLUE,
                        border_radius=ft.border_radius.all(0),
                    )
                )
            column = ft.Column(spacing=0, controls=items)
            tabla.append(ft.Column([ ft.Text(""), column]))
        return tabla
    
    page.add(
        ft.Row(
            #controls=[col1, col2],
            controls=generarTabla(matriz),
            spacing=0,  # Espacio entre columnas
            alignment=ft.MainAxisAlignment.START
        )
    )


ft.app(main)
