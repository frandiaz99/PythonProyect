import PySimpleGUI as sg
import os
import src.menu_principal as menu
import src.generador_memes as memes
import json
import src.paths
from src.paths import DIR_PROYECTO


def crear_window():
    """
    Crea los elementos del layout y la ventana.

    Returns
    -------
        PySimpleGUI.Window
    """

    json_path = os.path.join(DIR_PROYECTO, 'data', 'temples_memes.json')
    
    lista_temples= []
    with open(json_path, encoding='utf-8', mode = "r") as file:
        data = json.load(file)
        for elem in data:
            lista_temples.append(elem["name"])

    
    boton_volver=sg.Button("Volver", key="-VOLVER-",size=(13,2), pad=(0,10))
    
    boton_guardar= sg.Button("Generar", key="-GENERAR-",size=(13,2), pad=(0,10))
 
    
    layout = [[sg.Text("Generar Meme")],
              [sg.Text("Seleccionar Template")],
              [sg.Listbox (lista_temples, key='-TEMPLE_LISTADO-', expand_y=True, size=(20, 10), select_mode='single' )],
              [sg.Text(' ' * 7), boton_volver],
              [sg.Text(' ' * 7), boton_guardar]]

    
    selector_window = sg.Window("Generar Meme - UNLPImage", layout, margins=(15,30))
    return selector_window


def selector_memes(dicci):
    """
    Ejecuta y muestra en pantalla la ventana y maneja los eventos de la misma.

    Parameters
    ----------
    dicci: dict
        Diccionario con los datos de un único usuario.
    """
    window = crear_window()
    
    while True:        
        event, values = window.read()
        print(f"Evento: {event}, valores: {values}")
        
        match event:
            case '-VOLVER-':
                window.hide() 
                menu.menu_principal(dicci)                
                break            

            case '-GENERAR-':
                if values['-TEMPLE_LISTADO-'] != []:
                    window.hide()
                    print(values['-TEMPLE_LISTADO-'])
                    memes.generador_memes(dicci, values['-TEMPLE_LISTADO-'][0])                
                    break
                else:
                    sg.PopupOK('Por favor, seleccione un template del listado antes de continuar.')
            
            case sg.WIN_CLOSED:
                break        

    window.close()

if __name__== '__main__':
    selector_memes()     