import os
import json
import csv
import PySimpleGUI as sg
import PIL.ImageTk as ImageTk
import PIL.Image
import PIL.ImageDraw
import PIL.ImageOps as ImageOps
import src.diseño_collage as diseño
from src.paths import DIR_PROYECTO, convertir_para_guardar, convertir_guardado_para_usar
import src.log_system as logs
import src.configuracion as config

IMG_SIZE= 400,400

def get_collages_folder ():
    """intenta abrir el json de configuracion para 
        obtener la carpeta donde guardar los collages

    Returns
    -------
        str
    
    Raises
    ------
        FileNotFoundError
    """
    config_path= os.path.join(DIR_PROYECTO, 'data', 'config.json')
    try:
        with open(config_path) as file:
            paths= json.load(file)
            collages_path=convertir_guardado_para_usar(paths["collages"], DIR_PROYECTO)

    except FileNotFoundError:
        paths= dict([('imagenes', os.path.join(DIR_PROYECTO, 'imagenes')),
                     ('collages', os.path.join(DIR_PROYECTO, 'collages')),
                     ('memes', os.path.join(DIR_PROYECTO, 'memes'))])
        config.crear_config(config_path, paths)
    return collages_path

def get_imagenes_etiquetadas():
    """Abre el archivo de etiquetas.csv y copia las rutas
        de todas las imagenes etiquetadas en una lista 

    Returns 
    -------
        list
    
    Raises
    ------
        FileNotFoundError
    """
    etiquetas_csv_path= os.path.join (DIR_PROYECTO, 'data', 'etiquetas.csv')
    try:
        with open(etiquetas_csv_path) as file:
            csvreader= csv.reader(file, delimiter=',')
            encabezado, datos = next(csvreader), list(csvreader)
            rutas_csv=[]
            for elem in datos:
                print(elem)
                rutas_csv.append(elem[0])
            print (f" RUTAS_CSV: {rutas_csv}")
    except FileNotFoundError:
        rutas_csv=[]

    return rutas_csv


def get_color(color):
    """Retorna el nombre del color seleccionado en inglés para poder
        aplicarlo correctamente al texto ingresado.

    Parameters
    ----------
    color_name: str
        Nombre en español del color de texto seleccionado.                
    Returns
    -------
        dict
    """
    color_dict = {'Negro': 'Black', 'Blanco': 'White', 'Rojo': 'Red',
                  'Azul': 'Blue', 'Amarillo': 'Yellow', 'Verde': 'Green',
                  'Naranja': 'Orange', 'Violeta': 'Purple', 'Rosa': 'Pink',
                  'Marrón': 'Brown'}
    return color_dict[color]

def update_title(values, img_original, text_box, window):
    """Toma un objeto imagen que recibe como parametro
        y devuelve otro objeto del mismo tipo con un texto agregado

    Parameters
    ----------
    values: dict
        valores ingresados por el usuario
    img_original: PIL.Image.Image
        collage de imagenes sin un titulo agregado
    text_box:dict
        coordenadas x1, y1, x2,y2 donde debera posicionarse el titulo
    window: PySimpleGUI.Window
        Ventana actual que esta ejecutandose 

    Returns
    -------
        PIL.Image.Image
    """
    text_color = get_color(values['-COLOR_SELECT-'])
    img_original_copy = img_original.copy()
    draw = PIL.ImageDraw.Draw(img_original_copy, "RGBA")
    draw.rectangle ([(text_box["top_left_x"], text_box["top_left_y"]),
                     (text_box["bottom_right_x"], text_box["bottom_right_y"])],
                     width=0, fill=None)
    draw.text ((text_box["top_left_x"], text_box["top_left_y"]),
               values['-TITULO-'], fill=text_color)
    new_collage = PIL.Image.alpha_composite(img_original, img_original_copy)

    window['-IMAGEN-'].update(data=ImageTk.PhotoImage(new_collage))

    return new_collage

def get_images_and_buttons(dicci_diseño, diseño_elegido):
    """Arma una lista con cada uno de los botones para seleccionar
        una cantidad de imagenes específico de acuardo al diseño elegido

    Parameters
    ----------
    dicci_diseño: dict
        diccionario con todos los datos del diseño elegido

    diseño_elegido: str
        numero de diseño elegido
    
    Returns
    -------
        list
    
    Raises
    ------
        FileNotFoundError
    """
    config_path= os.path.join(DIR_PROYECTO, 'data', 'config.json')
    try:
        with open (config_path) as file:
            data= json.load(file)
            # busco en el json la carpeta configurada de donde sacar las imagenes para el collage
            img_path=convertir_guardado_para_usar(data["imagenes"], DIR_PROYECTO)
            print(img_path)
    except FileNotFoundError:
        paths= dict([('imagenes', os.path.join(DIR_PROYECTO, 'imagenes')), 
                     ('collages', os.path.join(DIR_PROYECTO, 'collages')), 
                     ('memes', os.path.join(DIR_PROYECTO, 'memes'))])

        config.crear_config (config_path, paths)
        
    collages_list = []
    number = 0

    for elem in dicci_diseño[diseño_elegido]:
        clave=f'-IMG {number +1}-'
        img_button = sg.FileBrowse(button_text=f'seleccionar imagen {number +1}',
                                   initial_folder=img_path,
                                   key=clave, enable_events=True)
        collages_list.append([img_button])
        number = number +1

    return  collages_list

def crear_window(dicci_dieseño, diseño_elegido):
    """Crea la ventana para la generacion de collage
    Parameters
    ----------
    dicci_diseño: dict
        diccionario con todos los datos del diseño elegido

    diseño_elegido: str
        numero de diseño elegido
    
    Returns
    -------
        PySimpleGUI.Window
    """
    collages_list= get_images_and_buttons(dicci_dieseño, diseño_elegido)
    color_list = ['Negro', 'Blanco', 'Rojo', 'Azul', 'Amarillo',
                  'Verde', 'Violeta', 'Naranja', 'Rosa', 'Marrón']
    color_dropdown = sg.Combo(key= '-COLOR_SELECT-',
                              values= color_list,
                              default_value= 'Negro',
                              size= (15, 1),
                              readonly= True)

    boton_volver=sg.Button("Volver", key="-VOLVER-", pad=(0,20))
    boton_guardar= sg.Button("Guardar Cambios", key="-GUARDAR_CAMBIOS-", pad=(0,20))

    columna_1 = [[sg.Image ( key ='-IMAGEN-', enable_events=True)]]
    columna_2= [[sg.Text("ingrese un titulo: ", font=('bookman', 16))],
                [sg.Push(), sg.InputText(enable_events=True, key='-TITULO-'),
                 sg.Button (button_text='Cargar', key='-CARGAR-')],
                 [sg.Push(), color_dropdown]
                 ]


    layout=[[sg.Text("Diseño de collage", font=('bookman', 20)),
             sg.Text(' '*135), boton_volver,sg.Text(' '), boton_guardar],
             [sg.Column(columna_1), sg.Column(columna_2)],
             [collages_list]
            ]
    # Creamos el objeto ventana
    editar_window = sg.Window("Generar collage: ", layout,
                              margins=(15,30), finalize=True,
                              element_justification='left')
    return editar_window

def get_size(dicci_dieseño, diseño_elegido):
    """Devuelve el tamaño que ocupa cada una de 
        las imagenes del collage
        
    Parameters
    ----------
    dicci_diseño: dict
        diccionario con todos los datos del diseño elegido

    diseño_elegido: str
        numero de diseño elegido
    Returns
    -------
        dict
    """
    # cantidad de imagenes
    cant= 1
    dicci_images={}

    for imagen in dicci_dieseño[diseño_elegido]:
        for elem in imagen.values():
            x1 = imagen["top_left_x"]
            x2 = imagen["bottom_right_x"]
            y1 = imagen["top_left_y"]
            y2 = imagen['bottom_right_y']
            x = x2-x1
            y = y2-y1
            # guardo la imagen en el dicci de imagenes
            dicci_images[f'img_{cant}'] = [x,y]

        cant+=1
        # dicci images tiene el tamaño que va a ocupar cada imagen en el collage
    return dicci_images

def resize_img(ruta_imagen, start_point):
    """Ajusta el tamaño de la imagen para que entre en el collage

     Parameters
     ----------
     ruta_imagen: str
        ruta de la imagen a pegar en el collage
     start_point: list
        valores xy donde debe comenzar la imagen 

     Returns
     -------
        PIL.Image.Image
    """
    img = PIL.Image.open(ruta_imagen)
    new_img = ImageOps.fit(img,(start_point[0], start_point[1]))
    return new_img

def get_data ():
    """Abre el json con la informacion de todos los diseños 
    y retorna el contenido en una variable 

    Returns 
    -------
        dict 
    """
    json_path =os.path.join(DIR_PROYECTO, 'data', 'diseños_collage.json')
    with open(json_path, encoding='utf-8', mode='r') as file:
        data = json.load(file)

    return data

def save_collage(collages_path, imagen_original_con_titulo):
    """Guarda el collage generado en formato jpg o png
    Parameters
    ----------
    collages_path: str
        Ruta de la carpeta donde se guardaran los collages
    imagen_original_con_titulo: PIL.Image.Image
        Imagen que se guardara en la carpeta especificafa
    
    Returns
    -------
        boolean
    """
    name = sg.popup_get_text("ingrese nombre para guardar el collage: ")
    file_extension = sg.Popup('Seleccione el formato de la imagen a guardar: ',
                              custom_text= ('jpg', 'png', 'Cancelar'))
    if file_extension:
        name = name + '.PNG'
        ruta_collage = os.path.join(collages_path, name)
        imagen_original_con_titulo.save(ruta_collage)
        sg.popup_ok ("la imagen ha sido guardada")
        return True
    else:
        sg.popup("por favor seleccione un formato de imagen")
        return False

def imagenes_cargadas(dicci_diseño, values):
    """Verifica que todas las imagenes que debe llevar
        el diseño hayan sido cargadas
    
    Parameters
    ----------
    dicci_diseño:list
        lista de diccionarios donde cada diccionario tiene las cordenadas de cada
        una de las imagenes del collage
    values: dict
        valores ingresados por el usuario

    Returns
    -------
        boolean
    """
    num_imagen = 1
    todas_cargadas = True

    for elem in dicci_diseño:
        if not values[f'-IMG {num_imagen}-']:
            todas_cargadas = False

        num_imagen += 1

    return todas_cargadas

def generador_collage(dicci_user, img):
    """
    Ejecuta y muestra en pantalla la ventana y maneja los eventos de la misma.

    Parameters
    ----------
    dicci_user: dict
        Diccionario con los datos de un único usuario.
    img: str
        str que representa el diseño de collage seleccionado.
    """
    data_json = get_data()
    num_diseño = int(img.split('_')[1])
    window = crear_window(data_json[num_diseño -1], img)

    collage = PIL.Image.new("RGBA", IMG_SIZE, color='white')
    imagen_original = collage.copy()
    imagen_original_con_titulo = collage.copy()

    window['-IMAGEN-'].update(data= ImageTk.PhotoImage(collage))

    collages_path = get_collages_folder()
    rutas_csv = get_imagenes_etiquetadas()

    while True:
        event, values = window.read()
        print(f"_________EVENT: {event}________")

        coordinates = {}
        coordinates = get_size(data_json[num_diseño -1], img)
        data_diseño = data_json[num_diseño -1][img]

        match event:
            case '-VOLVER-':
                volver = sg.popup_yes_no ("¿Volver a la pantalla de seleccion de diseño?")
                if volver == 'Yes':
                    window.hide()
                    diseño.diseño_collage(dicci_user)
                    break
            case '-IMG 1-':
                ruta = convertir_para_guardar(values['-IMG 1-'], DIR_PROYECTO)
                if ruta in rutas_csv:
                    size = [coordinates['img_1'][0], coordinates['img_1'][1]]
                    # ajusto el tamaño de la imagen al que yo le asigne en el collage
                    new_img_1 = resize_img(values['-IMG 1-'], size)
                    coordinates_img_1 = data_diseño[0]

                    imagen_original.paste(new_img_1, (coordinates_img_1['top_left_x'],
                                                      coordinates_img_1['top_left_y']))
                    window['-IMAGEN-'].update(data=ImageTk.PhotoImage(imagen_original))

                    if ((values['-TITULO-'])
                        and (not values['-TITULO-'].isspace())):
                        text_box = data_json[num_diseño-1]['text_boxes']
                        imagen_original_con_titulo = update_title(values,
                                                                  imagen_original,
                                                                  text_box, window)
                else:
                    sg.popup('La imagen seleccionada no ha sido etiquetada'
                             +'\n Por favor etiquetela antes de usarla')

            case '-IMG 2-':
                ruta = convertir_para_guardar(values['-IMG 2-'], DIR_PROYECTO)
                if ruta in rutas_csv:
                # me quedo con las coordenadas que abarca la segunda imagen del collage
                    size = [coordinates['img_2'][0], coordinates['img_2'][1]]
                    #ajusto el tamaño de la imagen al que yo le asigne en el collage
                    new_img_2 = resize_img(values['-IMG 2-'], size)
                    coordinates_img_2 = data_diseño[1]
                    imagen_original.paste(new_img_2, (coordinates_img_2['top_left_x'],
                                                      coordinates_img_2['top_left_y']))
                    window['-IMAGEN-'].update(data=ImageTk.PhotoImage(imagen_original))
                    if ((values['-TITULO-'] )
                        and (not values['-TITULO-'].isspace())):
                        text_box = data_json[num_diseño-1]['text_boxes']
                        imagen_original_con_titulo = update_title(values,
                                                                  imagen_original,
                                                                  text_box,
                                                                  window)

                # actualizo la ventana con el collage modificado
                else:
                    sg.popup('La imagen seleccionada no ha sido etiquetada'
                             +'\n Por favor etiquetela antes de usarla')

            case '-IMG 3-':
                ruta=convertir_para_guardar(values['-IMG 3-'], DIR_PROYECTO)
                if ruta in rutas_csv:
                    # me quedo con las coordenadas que abarca la tercera imagen del collage
                    size = [coordinates['img_3'][0], coordinates['img_3'][1]]
                    # ajusto el tamaño de la imagen al que yo le asigne en el collage
                    new_img_3 = resize_img(values['-IMG 3-'], size)
                    coordinates_img_3 = data_diseño[2]
                    imagen_original.paste(new_img_3,
                                          (coordinates_img_3['top_left_x'],
                                           coordinates_img_3['top_left_y']))
                    window['-IMAGEN-'].update(data=ImageTk.PhotoImage(imagen_original))

                    if ((values['-TITULO-'] )
                        and (not values['-TITULO-'].isspace())):
                        text_box = data_json[num_diseño-1]['text_boxes']
                        imagen_original_con_titulo = update_title(values,
                                                                  imagen_original,
                                                                  text_box,
                                                                  window)
                    # actualizo la ventana con el collage modificado
                else:
                    sg.popup('La imagen seleccionada no ha sido etiquetada'
                             +'\n Por favor etiquetela antes de usarla')
            case '-IMG 4-':
                ruta = convertir_para_guardar(values['-IMG 4-'], DIR_PROYECTO)
                if ruta in rutas_csv:
                    # me quedo con las coordenadas que abarca la cuarta imagen del collage
                    coordinates_img_4= data_diseño[3]
                    print (f"coordinates img 4 {coordinates_img_4}")
                    size = [coordinates['img_4'][0], coordinates['img_4'][1]]
                    # ajusto el tamaño de la imagen al que yo le asigne en el collage
                    new_img_4 = resize_img(values['-IMG 4-'], size)
                    imagen_original.paste(new_img_4,
                                          (coordinates_img_4['top_left_x'],
                                           coordinates_img_4['top_left_y']))
                    # actualizo la ventana con el collage modificado
                    window['-IMAGEN-'].update(data = ImageTk.PhotoImage(imagen_original))
                    if ((values['-TITULO-'] )
                        and (not values['-TITULO-'].isspace())):
                        text_box = data_json[num_diseño-1]['text_boxes']
                        imagen_original_con_titulo = update_title(values,
                                                                  imagen_original,
                                                                  text_box,
                                                                  window)
                else:
                    sg.popup('La imagen seleccionada no ha sido etiquetada'
                             +'\n Por favor etiquetela antes de usarla')
            case '-CARGAR-':
                if (values['-TITULO-'] ) and (not values['-TITULO-'].isspace()):
                    text_box = data_json[num_diseño-1]['text_boxes']
                    imagen_original_con_titulo = update_title(values,
                                                              imagen_original,
                                                              text_box,
                                                              window)
                    # actualizo la ventana con el collage modificado
                    window['-IMAGEN-'].update(data=ImageTk.PhotoImage(imagen_original_con_titulo))
                else:
                    sg.popup ("ingrese un titulo valido")

            case '-GUARDAR_CAMBIOS-':
                if imagenes_cargadas(data_diseño, values):
                    if (values['-TITULO-']
                        and not values['-TITULO-'].isspace()):
                        if save_collage(collages_path, imagen_original_con_titulo):
                            images_names = ''
                            number = 1
                            for nom in data_diseño:
                                path_img = convertir_para_guardar(
                                    values[f'-IMG {number}-'], DIR_PROYECTO)
                                images_names += path_img.split("/")[1] + ';'
                                number += 1
                                user=list(dicci_user.keys())[0]
                                logs.log_system(user,
                                                "Generacion de collage",
                                                images_names,
                                                values['-TITULO-'])
                    else:
                        sg.popup("por favor ingrese un titulo")
                else:
                    sg.popup("Por favor cargue todas las imagenes ")

            case sg.WIN_CLOSED:
                break 
    # Cerramos la ventana
    window.close()

if __name__== '__main__':
    generador_collage()
