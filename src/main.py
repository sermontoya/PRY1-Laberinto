import flet as ft
from pantalla_laberinto import pantalla_laberinto, setDimension

dimensionCache = "5x5"

def main(page: ft.Page):
    page.window.maximized = True
    page.title = 'Laberinto limonense'
    page.fonts = {
        'Jersey 25': 'fonts/Jersey25-Regular.ttf',
        'Jersey 20': 'fonts/Jersey20-Regular.ttf'
    }

    def route_change(route):
        page.views.clear()

        dimensiones_dropdown = ft.Dropdown(
            options=[
                ft.dropdown.Option("5x5"),
                ft.dropdown.Option("10x10"),
                ft.dropdown.Option("15x15"),
                ft.dropdown.Option("20x20"),
                ft.dropdown.Option("25x25"),
            ],
            scale=3,
            bgcolor=ft.Colors.with_opacity(1, '#182C61'), 
            color=ft.Colors.WHITE,
            text_style=ft.TextStyle(font_family='Jersey 25', size=14),
        )

        dimensiones_dropdown.value = dimensionCache

        def goLaberinto(e):
            global dimensionCache
            setDimension(dimensiones_dropdown.value)
            dimensionCache= dimensiones_dropdown.value
            page.go('/laberinto')


        page.views.append(
            ft.View(
                '/',
                [
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content = ft.Column(
                            controls=[
                                ft.Text('Laberinto limonense', size=96, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                ft.FilledButton('Iniciar', 
                                    icon=ft.Icons.ARROW_FORWARD, 
                                    on_click=lambda e: page.go('/modos'), 
                                    scale=3.5, 
                                    bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                                    color=ft.Colors.WHITE, 
                                    icon_color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                                    )
                                ),
                                ft.FilledButton('Salir', 
                                    icon=ft.Icons.EXIT_TO_APP, 
                                    on_click=lambda e: page.window.close(), 
                                    scale=3.5,
                                    bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                                    color=ft.Colors.WHITE, 
                                    icon_color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=150,
                        )
                    ),
                    ft.Container(
                        alignment=ft.alignment.bottom_right,
                        content=ft.FloatingActionButton(
                            icon=ft.Icons.INFO,
                            bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                            on_click=lambda e: page.go('/creditos')
                        ),
                        padding=20
                    )
                ]
            )
        )

        if page.route == '/modos':
            page.views.append(
                ft.View(
                    '/modos',
                    [
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content = ft.Column(
                            controls=[
                                ft.Text('Modos', size=96, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                ft.Row(
                                    controls=[
                                        ft.FilledButton('Automático', 
                                            icon=ft.Icons.GAMEPAD, 
                                            on_click=lambda e: page.go('/dimensiones'), 
                                            scale=3.5, 
                                            bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                                            color=ft.Colors.WHITE, 
                                            icon_color=ft.Colors.WHITE,
                                            style=ft.ButtonStyle(
                                                text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                                            )
                                        ),
                                        ft.FilledButton('Manual  ', 
                                            icon=ft.Icons.MOUSE, 
                                            on_click=lambda e: page.go('/dimensiones'), 
                                            scale=3.5, 
                                            bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                                            color=ft.Colors.WHITE, 
                                            icon_color=ft.Colors.WHITE,
                                            style=ft.ButtonStyle(
                                                text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=320
                                ),
                                ft.FilledButton('Volver', 
                                    icon=ft.Icons.ARROW_BACK, 
                                    on_click=lambda e: page.go('/'),
                                    scale=3.5,
                                    bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                                    color=ft.Colors.WHITE, 
                                    icon_color=ft.Colors.WHITE,
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=150,
                        )
                    )
                ]
                )
            )

        elif page.route == '/dimensiones':
            page.views.append(
                ft.View(
                    '/dimensiones',
                    [
                    ft.Container(
                        expand=True,
                        alignment=ft.alignment.center,
                        content = ft.Column(
                            controls=[
                                ft.Text('Dimensiones', size=96, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                dimensiones_dropdown,
                                ft.Row(
                                    controls=[
                                        ft.FilledButton('Volver', 
                                            icon=ft.Icons.ARROW_BACK, 
                                            on_click=lambda e: page.go('/modos'), 
                                            scale=3.5, 
                                            bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                                            color=ft.Colors.WHITE, 
                                            icon_color=ft.Colors.WHITE,
                                            style=ft.ButtonStyle(
                                                text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                                            )
                                        ),
                                        ft.FilledButton('Jugar', 
                                            icon=ft.Icons.PLAY_ARROW, 
                                            on_click=goLaberinto, 
                                            scale=3.5, 
                                            bgcolor=ft.Colors.with_opacity(0.5, '#182C61'), 
                                            color=ft.Colors.WHITE, 
                                            icon_color=ft.Colors.WHITE,
                                            style=ft.ButtonStyle(
                                                text_style=ft.TextStyle(font_family='Jersey 25', size=14)
                                            )
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=320
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=200,
                        )
                    )
                ]
                )
            )
        
        elif page.route == "/laberinto":
            page.views.append(pantalla_laberinto(page))

        elif page.route == "/creditos":
            page.views.append(
                ft.View(
                    '/creditos',
                    [
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    expand=True,
                                    alignment=ft.alignment.center,
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.Icon(name=ft.Icons.CODE, size=96, color=ft.Colors.with_opacity(0.75, '#182C61')),
                                                    ft.Text('Creditos', size=96, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                                    ft.Icon(name=ft.Icons.CODE_SHARP, size=96, color=ft.Colors.with_opacity(0.75, '#182C61'))
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            ft.Divider(),
                                            ft.Text('Desarrolladores', size=48, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                            ft.Text('Sergio Montoya Badilla', size=24, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                            ft.Text('Johnsy Lopez Aguilar', size=24, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                            ft.Text(' ', size=24, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                            ft.Text('Profesor', size=48, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                            ft.Text('Jose Angel Campos Aguilar', size=24, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                            ft.Text(' ', size=24, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                            ft.Text('Creado por estudiantes del TEC con mucho sueño en Semana Santa', size=24, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                            ft.Text(' ', size=24, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                            ft.Text('Laberinto limonense. Todos los derechos reservados 2025.', size=14, weight=ft.FontWeight.BOLD, font_family='Jersey 25'),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=35,
                                    )
                                ),
                                ft.Container(
                                    content=ft.FloatingActionButton(
                                        icon=ft.Icons.ARROW_BACK,
                                        on_click=lambda _: page.go('/'),
                                        bgcolor=ft.Colors.with_opacity(0.5, '#182C61'),
                                        shape=ft.CircleBorder(),
                                        scale=1.5
                                    ),
                                    alignment=ft.alignment.top_left,
                                    margin=30
                                )
                            ]
                        )
                    ]
                )
            )

        
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, assets_dir="assets")