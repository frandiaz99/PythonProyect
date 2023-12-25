import os
import json
import PySimpleGUI as sg
import src.configuracion as config
import src.log_system as logs
from src.paths import DIR_PROYECTO, convertir_guardado_para_usar, convertir_para_guardar
def genero(values, window):
    """ Verifica que se haya ingresado un genero ya sea de los brindados
        en la 'lista_generos' o por teclado

    Parameters
    ---------
    values: dict
        diccionario con los valores ingresados por teclado
    window: PySimpleGUI.Window
        ventana actual

    Returns
    ------
        str
    """
    if values['-GENERO_INPUT-'] != "":
        return values ['-GENERO_INPUT-']
    elif len (values['-GENERO_LISTADO-']) != 0:
        return values['-GENERO_LISTADO-'][0]
    else:
        genero = sg.popup_get_text("Por favor ingrese un genero: ")
        window['-GENERO_INPUT-'].update(genero)

        return genero

def avatar(values, window, avatar_default_path):
    """ Verifica si se selecciono otro avatar distinto al por defecto,
        de ser verdadero lo actualiza en la ventana

    Parameters
    ---------
    values: dict
        diccionario con los valores ingresados por teclado
    window: PySimpleGUI.Window
        ventana actual
    avatar_defaul_path: str
        str que representa la ruta del avatar por defecto.

    Returns
    ------
        str
    """
    if values['-AVATAR-']== "":
        return convertir_para_guardar(avatar_default_path, DIR_PROYECTO)
    else:
        window['-AVATAR_DEFAULT-'].update(values['-AVATAR-'])
        return convertir_para_guardar(values['-AVATAR-'], DIR_PROYECTO)

def save_data(nick, dicci, tipo):
    """ Guarda los datos ingresados en el json 'perfiles',
    en caso que este no exista, lo crea

    Parameters
    ---------
    nick: str
        str que representa el nick del usuario.
    dicci: dict
        diccionario con los datos del nuevo usuario a guardar 
    tipo: str
        str que contiene el modo en el que se abre el archivo
    """
    full_path = os.path.join(DIR_PROYECTO,'data', 'perfiles.json')

    with open (full_path, tipo) as archivo:
        json.dump(dicci, archivo, indent=4)

    logs.log_system(nick, 'Creación de nuevo perfil')

def fields_validation (dicci):
    """ Verifica que se hayan completado todos los campos

    Parameters
    ---------
    dicci: dict
        diccionario con los datos del usuario
    Returns
    ------
        boolean
    """
    for elem in dicci.values():
        for val in elem.values():
            if (val and not val.isspace()):
                return True
            else:
                sg.popup("Aún hay campos vacios, por favor complete todos los campos", title=None)
                return False

def age_validation(edad):
    """Verifica que la cadena ingresada en el campo 'Edad' sean unicamente digitos numericos

    Parameters
    ---------
    edad: string
        cadena que representa la edad ingresada por el usuario
    Returns
    ------
        boolean
    """
    if edad.isdigit():
        return True
    else:
        sg.popup("la edad deben ser solo digitos numericos")
        return False

def nick_validation (nick, valores):
    """Verifica que el nick ingresado no este en uso

        Parameters
        ----------
        nick: string
            string ingresado por teclado
        valores: dict
            diccionario con los valores ingresados por teclado
        
        Returns
        -------     
            boolean

        Raises
        ------
            FileNotFoundError
    """
    data_path = os.path.join (DIR_PROYECTO, 'data')
    full_path = os.path.join(DIR_PROYECTO,'data', 'perfiles.json')
    try:
        with open (full_path, encoding='utf-8', mode= "r" ) as archivo:
            perfiles= json.load (archivo)

            if nick not in perfiles:
                perfiles[nick] = valores
                save_data (nick, perfiles, "w")
                return True
            else:
                sg.popup("Este nick ya esta en uso por favor seleccione otro")
                return False

    except FileNotFoundError:
        archivo = open(os.path.join(data_path, 'perfiles.json'), "w")
        save_data(nick, dict([(nick, valores)]), "w")
        full_path= os.path.join(DIR_PROYECTO, 'data', 'config.json')
        paths = config.get_paths(full_path)
        config.crear_config(full_path, paths)
        return True
