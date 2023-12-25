import PySimpleGUI as sg
import os
import json
import src.log_system as logs
from src.paths import DIR_PROYECTO

def abrir_json():
    """
        Funcion para abrir el json.

        Returns
        -------
            dict        
    """
    
    file_json= os.path.join(DIR_PROYECTO,'data','perfiles.json')

    with open (file_json, encoding='utf-8', mode= "r" ) as archivo:            
            perfiles= json.load (archivo)
    return perfiles      


def genero(values,gen): 
    """
        Verifico si se produjo el evento otro, que hace referencia al checkbox para marcar otro genero
        y se asigna el genero ingresado al campo referente al genero.

        Parameters
        ----------
        values: str
            Contiene los valores que se produjeron en windows.
        gen: str
            Contiene el genero autopercivido por defecto del usuario.
        
        Returns 
        -------
            str  
    """

    if values['-OTRO-']:
        if not values['-GENERO_INPUT-'].isspace() and values['-GENERO_INPUT-'] != '':
            return values['-GENERO_INPUT-']
        else:
            sg.PopupOK('texto vacio, intente denuevo:')
    else: 
        if len (values['-GENERO_LISTADO-'])== 0:
            return gen
        else:
            return values['-GENERO_LISTADO-'][0]
            
        
def edi_avatar(values,avat):
    """
        se verifica que al avatar selecionado no sea vacio
        
        Parameters
        ----------
        values: str
            Contiene los valores que se produjeron en windows. 
        avat: str
            Nuevo avatar seleccionado 
        
        Returns 
        -------
            str  
    """

    if values['-AVATAR-']== "":
        return avat
    else: 
        return values['-AVATAR-']
    
def validar_valores(dicci):
    """
        se valida que se hayan completado todos los campos relacionados a los 
        datos del usuario.

        Parameters
        ----------
        dicci: dict
            Diccionario con los valores del usuario.
        Returns 
        -------
            boolean    
    """

    for elem in dicci.values(): 
        for val in elem.values(): 
            if not (val and not val.isspace()): 
                sg.popup("por favor complete todos los campos")
    return True   
   
def guardar_cambios(nick,valores):
    """
        se guarda en el json los valores del usuario ingresados por parametros.
        
        Parameters
        ----------
        nick: str
             nick del usuario.
        valores: dict
            Diccionario con los valores ingresados y/o modoficados.
    """
    file_json= os.path.join(DIR_PROYECTO,'data','perfiles.json')

    perfiles=[]
    with open(file_json, "r")as file:
        perfiles=json.load(file)
        print(perfiles)
    perfiles[nick]=valores
    with open(file_json, "w")as file:
        json.dump(perfiles, file, indent=4)
    
    logs.log_system(nick, 'Modificación de perfil')
    