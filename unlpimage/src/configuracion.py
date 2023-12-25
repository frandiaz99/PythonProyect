import os
import json
import PySimpleGUI as sg
import src.menu_principal as menu
import src.log_system as log
from src.paths import DIR_PROYECTO, convertir_guardado_para_usar, convertir_para_guardar

sg.theme('LightBrown9')
sg.set_options(font='bookman 12')

def crear_config (json_path, paths):
    """ Crea el archivo 'config.json' con los valores recibidos a traves del parametro 'paths'

    Parameters
    ---------
    paths: dict
        diccionario con las rutas de las carpetas a utilizar como directorio de imagenes, 
        repositorio de collage y repositorio de memes  
    json_path: str
        ruta donde se guardara el json 

    Returns
    ------
        dict
    """
   #creo archivo config con valores recibidos en el diccionario paths
    default_paths ={}
    default_paths= dict(
                    map(lambda item:(item[0], (convertir_para_guardar(item[1], DIR_PROYECTO))),
                        paths.items())
                        )

    with open(json_path,"w") as archivo:
        json.dump(default_paths, archivo, indent=4)

def get_paths(json_path):
    """Obtiene los paths del directorio de imagenes, del repositorio collage y del repositorio
    de memes 

    Parameters
    ---------
    json_path: str
        ruta del archivo 'config.json'

    Returns
    ------
        dict
    Raises
    ------
        FileNotFoundError
    """
    paths={}
    try:
        # si el archivo 'config.json' ya existe entonces tengo que convertir los paths
        with open (json_path, "r") as archivo:
            default_paths= json.load(archivo)
            for folder, relative_path in default_paths.items():
                paths[folder]=convertir_guardado_para_usar(default_paths[folder],DIR_PROYECTO )
                return paths
    except FileNotFoundError:
        # si el archivo config.json fue borrado, creo uno con las rutas por defecto
        paths = dict([('imagenes', os.path.join(DIR_PROYECTO, 'imagenes')),
                     ('collages', os.path.join(DIR_PROYECTO, 'collages')),
                     ('memes', os.path.join(DIR_PROYECTO, 'memes'))])
        crear_config (json_path, paths)
        return paths

def create_window(paths):
    """Crea los elementos del layout y la ventana.

    Parameters
    ----------
    paths: dict
        diccionario con las rutas de las carpetas configuradas como directorio de imagenes, 
        repositorio de collages y repositorio de memes
    Returns
    -------
        PySimpleGUI.Window
    """
    layout_paths=[]
    for folder, relative_path in paths.items():
        layout_paths.append([sg.Push(),sg.Text(f'Directorio de {folder} :'), sg.Push(),
                             sg.Input(key= f'-{folder}_input-', default_text= relative_path),
                             sg.FolderBrowse(button_text= 'Seleccionar',
                                             key=f'-repositorio_{folder}-',
                                             initial_folder= relative_path, enable_events=True),
                                             sg.Push()])
    column1= sg.Column(layout_paths)
    column2= [[sg.Text("CONFIGURACION: "), sg.Push()],
              [sg.Push(), sg.Text('', ), sg.Push()],
              [column1],
              [sg.Push(), sg.Button('Volver', key= '-VOLVER-' ),
               sg.Button('Guardar', key='-GUARDAR-'), sg.Push()]
              ]

    layout = [[sg.Push(), sg.Column(column2), sg.Push()]]
    window= sg.Window ("Configuracion", layout)
    return window

def configuracion(user_data):
    """
    Ejecuta y muestra en pantalla la ventana y maneja los eventos de la misma.

    Parameters
    ----------
    user_Data: dict
        Diccionario con los datos de un único usuario.

    Raises
    ------
        AttributeError
    """
    json_path = os.path.join (DIR_PROYECTO, 'data', 'config.json')

    paths = get_paths(json_path)
    window = create_window(paths)

    while True:
        event, values= window.read()
        if values['-imagenes_input-']:
            window['-imagenes_input-'].update(convertir_guardado_para_usar
                                              (values['-imagenes_input-'], DIR_PROYECTO))
        if values['-collages_input-']:
            window['-collages_input-'].update(convertir_guardado_para_usar
                                              (values['-collages_input-'], DIR_PROYECTO))
        if values['-memes_input-']:
            window['-memes_input-'].update(convertir_guardado_para_usar
                                            (values['-memes_input-'], DIR_PROYECTO))
        if event == '-VOLVER-':
            window.hide()
            menu.menu_principal(user_data)
            break
        if event =='-GUARDAR-':
            new_paths={}
            try:
                if (values['-imagenes_input-']
                    and not values['-imagenes_input-'].isspace()):
                    new_paths['imagenes'] = convertir_para_guardar(
                                            values['-imagenes_input-'], DIR_PROYECTO)

                if (values ['-collages_input-']
                    and not values['-collages_input-'].isspace()):
                    new_paths['collages']= convertir_para_guardar (
                                            values['-collages_input-'], DIR_PROYECTO)

                if (values['-memes_input-']
                    and not values['-memes_input-'].isspace()):
                    new_paths ['memes']= convertir_para_guardar (
                                            values ['-memes_input-'], DIR_PROYECTO)

            except AttributeError :
                sg.popup("La ruta especificada no es correcta")

            confirmacion=  sg.popup_yes_no("Esta seguro que desea guardar los cambios?")
            if confirmacion == 'Yes':
                with open (json_path, "w") as archivo:
                    json.dump(new_paths, archivo,  indent=4)

                lista= list(user_data.keys())
                log.log_system(lista[0], "Cambio en la configuración del sistema")
                window.hide()
                menu.menu_principal(user_data)
                break

        if event == sg.WIN_CLOSED:
            break

    window.close()

if __name__ =='__main__':
    configuracion()
