import os
import json
import PySimpleGUI as sg
from PIL import Image, ImageTk
import src.other.funciones as function
import src.menu_principal as menu
import src.inicio as inicio
from src.paths import DIR_PROYECTO, convertir_guardado_para_usar, convertir_para_guardar

sg.theme('LightBrown9')
sg.set_options(font='bookman 12')

def create_window(avatar_path, avatar_default_path): 
    """Crea la ventana  'nuevo perfil'

    Parameters
    ---------
        avatar_path: str
            ruta de la carpeta con las imagenes de los avatars
        avatar_default_path: str
            ruta del avatar por defecto

    Returns
    -------
        PySimpleGUI.Window
    """
    generos = ['mujer', 'hombre', 'no binario']

    text_column = [[sg.Text(" ")],
                  [sg.Push(), sg.Text ("Nick/ Alias : "),
                   sg.InputText(key = '-NICK-', size = (15,1))],
                   [sg.Push(), sg.Text ("Nombre: "), sg.InputText(key= '-NOMBRE-', size=(15,1) )],
                   [sg.Push(), sg.Text ("Edad: "), sg.Input( key='-EDAD-', size=(15,1))],
                   [sg.Push(), sg.Text ("Género autopercibido: " ),
                    sg.Listbox (generos, key='-GENERO_LISTADO-', expand_y=True, size=(10, 5),
                                select_mode='single' )],
                    [sg.Push(),  sg.Radio ("Otro","genero",  default=False )],
                    [sg.Push(), sg.InputText(key='-GENERO_INPUT-', size=(15,1),
                                             enable_events= True)]
                    ]
    layout = [[sg.Push(), sg.Text("NUEVO PERFIL"), sg.Push()],
              [[sg.Image (source=avatar_default_path, key='-AVATAR_DEFAULT-',
                           enable_events=True, size=(200,200)), sg.Text(' '*10),
                           sg.VSep(color='pink'),
                           sg.Column(text_column, element_justification='l')]],
                [sg.FileBrowse(button_text="Seleccionar Avatar", key='-AVATAR-', enable_events=True,
                                          initial_folder= avatar_path)],
                [[sg.Push(), sg.Button('Volver', key='-VOLVER-'),
                  sg.Button('Guardar', key= '-GUARDAR-'),
                  sg.Push()]],
            ]
    window= sg.Window (" ", layout, resizable=True)
    return window

def crear_perfil(): 
    """ Ejecuto la ventana de crear perfil
    """
    data_path= os.path.join(DIR_PROYECTO,'data')
    print (f"nuevo perfil -->data_path{data_path}")
    avatar_path = os.path.join(DIR_PROYECTO,'avatar')
    print (f"nuevo perfil --> avatar_path{avatar_path}")
    avatar_default_path = os.path.join(avatar_path, 'avatar_default.png')
    print (f"nuevo perfil --> avatar_default_path {avatar_default_path}")
    
    window= create_window(avatar_path, avatar_default_path)
    while True:
        event, values = window.read()
        match event:
            case sg.WIN_CLOSED:
                sg.popup_ok("Los cambios no han sido guardados", text_color = 'black', 
                            no_titlebar=True)
                break
            case other:
                if event == '-GUARDAR-':
                    valores= dict([('NOMBRE', values['-NOMBRE-']), ('EDAD', values['-EDAD-']),
                                   ('AVATAR', function.avatar(values, window, avatar_default_path)),
                                   ('GENERO', function.genero(values, window))])
                    dicci= dict([(values['-NICK-'], valores)])
                    if (function.fields_validation(dicci) 
                        and function.age_validation(values['-EDAD-'])):
                        if function.nick_validation(values['-NICK-'], valores):
                            window.hide()
                            menu.menu_principal(dicci)
                            break
                else:
                    if values['-AVATAR-'] != "":
                        window['-AVATAR_DEFAULT-'].update(values['-AVATAR-'])
                    if event == '-VOLVER-':
                        window.hide()
                        inicio.inicio()
                        break
    window.close()

if __name__ =='__main__': 
    crear_perfil()
