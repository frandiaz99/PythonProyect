import json
import os
import PySimpleGUI as sg
from src.menu_principal import menu_principal
from src.nuevo_perfil import crear_perfil
from src.paths import DIR_PROYECTO


def crear_ventana_principal(indice, data=None):
    """
    Crea los elementos del layout y la ventana Inicio.

    Parameters
    ----------
    indice: int
        Lleva la cuenta de cantidad de perfiles
    data: dict
        Archivo Json con perfiles.

    Returns
    -------
        PySimpleGUI.Window
    """

    path_img = os.path.join(DIR_PROYECTO, 'img', 'signoSuma.png')

    layout_perfiles = []

    texto_agregar_perfil = sg.Text(
        "Agregar perfil",
        justification="center",
        background_color='black',
        text_color="white"
    )

    boton_agregar_perfil = sg.Button(
        image_source=path_img,
        image_size=(64, 64),
        border_width=5,
        key="-PRINC-CREAR-PERFIL-",
        button_color=('black', 'white'),
        pad=((0, 0), (10, 0))
    )

    layout_agregar_perfil = [sg.Column(
        [
            [boton_agregar_perfil],
            [texto_agregar_perfil]
        ],
        element_justification='c',
        background_color='black'
    )]

    if indice > 0:
        layout_anterior = [sg.Button(
            "ANTERIOR ",
            border_width=5,
            key="-PRINC-VER-MENOS-",
            button_color=('black', 'white'),
            pad=((0, 0), (10, 0))
        )]
    else:
        layout_anterior = []

    if (data is not None):
        nick_list = list(data.keys())

        if len(nick_list) > indice + 4:
            layout_siguiente = [sg.Button(
                "VER MAS ", border_width=5,
                key="-PRINC-VER-MAS-",
                button_color=('black', 'white'),
                pad=((0, 0), (10, 0))
            )]
        else:
            layout_siguiente = []

        for perfil_key in nick_list[indice:indice + 4]:
            perfil = data[perfil_key]
            path_perfil = perfil["AVATAR"]
            print("avatar: " + path_perfil)
            boton_p = sg.Button(
                key=f"-PRINC-PERFIL-{perfil_key}-",
                    image_source=path_perfil,
                    image_size=(64, 64),
                    border_width=5,
                    tooltip=perfil_key,
                    button_color=('black', 'white'),
                    pad=((0, 0), (10, 0))
            )
            nombre_p = sg.Text(
                perfil_key,
                font=("Arial", 8),
                justification="center",
                background_color='black',
                text_color="white"
            )
            columna = sg.Column(
                [
                    [boton_p],
                    [nombre_p]
                ],
                element_justification="c",
                background_color='black'
            )
            layout_perfiles.append(columna)

            layout = [
                [sg.Text("UNLPImage",
                         font='Courier 12',
                         text_color='black',
                         background_color='white')
                 ],
                layout_perfiles + layout_agregar_perfil,
                layout_anterior + layout_siguiente,
            ]

    else:
        layout = [
            [sg.Text("UNLPImage",
                     font='Courier 12',
                     text_color='black',
                     background_color='white')
             ],
            layout_agregar_perfil,
        ]

    return sg.Window(
        "PRINCIPAL",
        layout,
        finalize=True,
        margins=(
            300,
            100),
        background_color='black')


def manejar_eventos_principal(ventana, evento, indice, data=None):
    """
    Maneja los eventos de la ventana de inicio.

    Parameters
    ------------

    ventana: PySimpleGUI.Window
        ventana actual en ejecucion
    evento: dict
        evento que salto de acurdo al boton o accion realizada
    indice: int
        Lleva la cuenta de cantidad de perfiles
    data: dict
        Archivo Json de perfiles

    Returns
    -------
        PySimpleGUI.Window
        int
    """

    if evento == "-PRINC-CREAR-PERFIL-":
        ventana.hide()
        crear_perfil()
        ventana.close()

    elif evento.startswith("-PRINC-PERFIL-"):
        ventana.hide()
        key = evento.split("-")[3]
        perfil = data[key]
        dicc = {}
        dicc[key] = perfil
        print(dicc)
        menu_principal(dicc)
        ventana.close()

    elif evento == "-PRINC-VER-MAS-":
        indice += 4
        if ventana.TKroot:
            ventana.close()
        ventana_principal = crear_ventana_principal(indice, data)
        return ventana_principal, indice

    elif evento == "-PRINC-VER-MENOS-":
        indice -= 4
        if ventana.TKroot:
            ventana.close()

        ventana_principal = crear_ventana_principal(indice, data)
        return ventana_principal, indice
    
    return None, None


def inicio():
    """
    Ejecuta y muestra en pantalla la ventana y maneja los eventos de la misma.

    Raises
    ----------
        FileNotFoundError
        UnboundLocalError

    """

    indice = 0
    json_path = os.path.join(DIR_PROYECTO, 'data', 'perfiles.json')

    try:
        with open(json_path, encoding='utf-8', mode="r") as file:
            data = json.load(file)
            ventana_principal = crear_ventana_principal(indice, data)

    except FileNotFoundError:
        ventana_principal = crear_ventana_principal(indice, None)

    data_collage = os.path.join(DIR_PROYECTO, 'data', 'diseños_collage.json')
    data_meme = os.path.join(DIR_PROYECTO, 'data', 'temples_memes.json')

    if (not os.path.isfile(data_collage)) or (not os.path.isfile(data_meme)):
        sg.PopupOK(f"No se encontraron alguno de los siguientes archivos en la carpeta 'data':\n  - 'diseños_collage.json'\n  - 'temples_memes.json'\n Por favor, verifique que existan antes de ejecutar el programa.")

    else:

        while True:
            window, event, values = sg.read_all_windows()
            print(
                f"ventana: {window},evento: {event}, valures: {values},ventana principal:  {ventana_principal}")

            if event == sg.WIN_CLOSED:
                if window is not None:
                    if window == ventana_principal:
                        window.close()
                    else:
                        window.hide()
                        window.close()
                        ventana_principal.un_hide()
                else:
                    ventana_principal.close()
                    break
            else:
                try:
                    new_window, indice = manejar_eventos_principal(
                        window, event, indice, data)
                except UnboundLocalError:  # en caso de que no hay perfiles en el json
                    new_window, indice = manejar_eventos_principal(
                        window, event, indice)
                if new_window:
                    ventana_principal = new_window


if __name__ == '__main__':
    inicio()
