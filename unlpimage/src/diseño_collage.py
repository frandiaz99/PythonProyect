import os
import json
import PySimpleGUI as sg
import src.menu_principal as menu
import src.generador_collage as collage
from src.paths import DIR_PROYECTO, convertir_guardado_para_usar, convertir_para_guardar

sg.set_options(font= 'bookman')
print (DIR_PROYECTO)

os_path= os.path.realpath('.')
img_folder_path=os.path.join(os_path,'img')

def get_imagenes_path():
    """Retorna el path de la carpeta en la cual se encuentran las imagenes con los
    diseños para el collage 

    Returns
    -------
        str
    """
    imagenes_path= convertir_guardado_para_usar('img', DIR_PROYECTO)
    return imagenes_path

def get_data_from_json():
    """ Copia la informacion de los diseños predefinidos en el json 
        en una variable que luego retorna

    Returns
    -------
        list
    """
    json_path =os.path.join(DIR_PROYECTO, 'data', 'diseños_collage.json')
    print (json_path)
    with open(json_path, encoding='utf-8', mode='r') as file:
        data_json= json.load(file)
    return data_json

def crear_lista_diseños (imagenes_path, data_json):
    """Crea una lista con las rutas de las imagenes de los diseños 

    Parameters
    ----------
    imagenes_path: str
        ruta de la carpeta con las imagenes de los diseños a mostrar
    data_json: list
        lista de diccionarios con la informacion de cada diseño de collage

    Returns 
    -------
        list
    """
    lista_diseños=[]

    for elem in data_json:
        img_path= os.path.join(imagenes_path, elem["image"])
        diseño= convertir_guardado_para_usar(img_path, DIR_PROYECTO)
        lista_diseños.append(diseño)
    return lista_diseños

def crear_window(imagenes_path,data_json):
    """Crea la ventana de seleccion de diseño con los elementos correspondientes 
     Parameters
    -----------
    imagenes_path: str
        ruta de la carpeta con las imagenes de los diseños a mostrar
    data_json: list
        lista de diccionarios con la informacion de cada diseño de collage

    Returns
    -------
        PySimpleGUI.Window        
    """

    boton_volver=sg.Button("Volver", key="-VOLVER-",size=(13,2), pad=(0,20))
    boton_avanzar= sg.Button("Generar collages", key="-AVANZAR-",
                             size=(13,2), pad=(0,20))
    layout_img=[]
    lista_diseños= crear_lista_diseños(imagenes_path, data_json)
    for diseño in lista_diseños:
        clave= (lista_diseños.index(diseño)) +1

        button_img= sg.Button (key= f'-DISEÑO {clave}-', image_source=diseño,)
        layout_img.append(button_img)

    layout=[
        [sg.Push(), sg.Text("Diseño de collage", key='-TITULO-',
                            font=('bookman' , 20)),sg.Text(' '*135),
                            boton_volver, sg.Push()],
        [sg.Text("Seleccione un diseño: ")],
        [layout_img],
        [sg.Push(), boton_avanzar]
        ]

    diseño_window = sg.Window("diseño: ", layout, margins=(15,30))
    return diseño_window

def diseño_collage(dicci_user):
    """
    Ejecuta y muestra en pantalla la ventana y maneja los eventos de la misma.

    Parameters
    ----------
    dicci_user: dict
        Diccionario con los datos de un único usuario.
    """
    imagenes_path= get_imagenes_path()
    data_json= get_data_from_json()
    window=crear_window(imagenes_path, data_json)

    while True:
        event, values = window.read()
        print(f"Evento: {event}, valores: {values}")
        match event:
            case '-VOLVER-':
                window.hide()
                menu.menu_principal(dicci_user)
                break
            case '-DISEÑO 1-':
                window.hide()
                collage.generador_collage(dicci_user, 'img_1')
                break
            case '-DISEÑO 2-':
                window.hide()
                collage.generador_collage(dicci_user, 'img_2')
                break
            case '-DISEÑO 3-':
                window.hide()
                collage.generador_collage(dicci_user, 'img_3')
                break
            case '-DISEÑO 4-':
                window.hide()
                collage.generador_collage(dicci_user, 'img_4')
                break

        if event == sg.WIN_CLOSED:
            break

    window.close()

if __name__== '__main__':
    diseño_collage()
 