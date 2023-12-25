import os
import json
import random
import string
import textwrap
from time import strftime
import PySimpleGUI as sg
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageTk
import src.selector_memes as memes
import src.log_system as logs
import src.paths
from src.paths import DIR_PROYECTO


def get_color(color_name):
    """
    Retorna el nombre del color seleccionado en inglés para poder aplicarlo correctamente al texto ingresado.

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

    print(f'El color es: {color_dict[color_name]}')
    return color_dict[color_name]


def get_image_data(my_template):
    """
    Abre un archivo .json para obtener los datos de la plantilla seleccionada del mismo.

    Parameters
    ----------
    my_template: str
        Nombre de la plantilla de memes seleccionada.                
    Returns
    -------
        dict
    """
    json_path = os.path.join(DIR_PROYECTO, 'data', 'temples_memes.json')

    img_data = {}

    with open(json_path, encoding='utf-8', mode = "r") as json_file:
        templates = json.load(json_file)

        for elem in templates:
            if elem['name'] == my_template:
                img_data = elem
    
    return img_data


def save_image(image, meme_name, current_user, img_name, texts):
    """
    Guarda la imagen del meme generado en formato jpg o png, en el directorio de memes.

    Parameters
    ----------
    image: PIL.PngImagePlugin.PngImageFile
        Imagen que se va a guardar.
    meme_name: str
        Nombre de la plantilla utilizada para generar el meme.
    current_user: str
        El nombre del usuario actual.
    img_name: str
        Nombre del archivo de imagen original utilizado como plantilla para generar el meme.
    window: PySimpleGUI.Window
        Ventana que se está ejecutando actualmente.

    Raises
    ------
        FileNotFoundError
    """
        
    file_extension = sg.Popup('Seleccione el formato de la imagen a guardar: ',
                                custom_text= ('jpg', 'png', 'Cancelar'))

    if file_extension == 'jpg' or file_extension == 'png':
        confirmation = sg.PopupYesNo(f'¿Desea generar y guardar el meme en formato {file_extension}?')

        if confirmation == 'Yes':            
            current_time = strftime(f'{meme_name}_%Y-%m-%d_%H-%M-%S')
            meme_filename = f'{current_time}.{file_extension}'
            
            
            config_path = os.path.join(DIR_PROYECTO, 'data', 'config.json')

            try:            
                with open(config_path, encoding= 'utf-8', mode = "r") as config_file:
                    config_data = json.load(config_file)
                    meme_path = os.path.join(DIR_PROYECTO, config_data['memes'], meme_filename)

                    if file_extension == 'jpg':
                        jpg_image = image.convert('RGB')
                        jpg_image.save(meme_path)
                
                    else:
                        image.save(meme_path)
                
                logs.log_system(current_user, 'Generación de meme', img_name, texts)
                sg.PopupOK(f'¡El meme {meme_filename} se ha guardado con éxito!')
            
            except FileNotFoundError:
                sg.PopupOK('Ocurrió un error al querer guardar el meme...\nPor favor, verifique que las rutas en el menú de Configuración sean correctas.')


def apply_text(image, text_boxes_sizes, values, window):
    """
    Dibuja uno o más textos sobre una imagen, calculando las posiciones donde lo hará sobre la misma.

    Parameters
    ----------
    image: PIL.PngImagePlugin.PngImageFile
        Imagen sobre la cual se va a dibujar.
    text_boxes_sizes: list
        Lista que contiene diccionarios con datos sobre las posiciones de los textos.
    values: dict
        Diccionario con distintos valores que se ingresan a través de la interfaz del programa.
    window: PySimpleGUI.Window
        Ventana que se está ejecutando actualmente.
                
    Returns
    -------
        PIL.PngImagePlugin.PngImageFile
    """
    width, height = image.size

    text_boxes_list = []
    key_list = []
    number = 0
    dicci = {}
    texts_completed = True
        
    for elem in text_boxes_sizes:

        number += 1
        text = values['-TEXT_INPUT_' + str(number) + '-']

        if text and not text.isspace():

            x1 = elem['top_left_x']  # Coordenada x inicial del rectángulo (10% del ancho)
            y1 = elem['top_left_y']  # Coordenada y inicial del rectángulo (40% del alto)
            x2 = elem['bottom_right_x']  # Coordenada x final del rectángulo (90% del ancho)        
            y2 = elem['bottom_right_y']  # Coordenada y final del rectángulo (60% del alto)

            key_list = list(dicci.keys())
            if text in key_list:
                new_text = f'{text}{(" " * number)}'
                dicci[new_text] = [x1, y1, x2, y2]
            else:
                dicci[text] = [x1, y1, x2, y2]

            text_boxes_list.append(dicci)

        else:
            sg.PopupOK('Hay textos sin completar. Por favor, vuelva a intentarlo.')
            texts_completed = False
            break

    if texts_completed:
        draw = ImageDraw.Draw(image)

        font_path = os.path.join(DIR_PROYECTO, 'data', 'fonts', values['-FONT_SELECT-'] + '.ttf')
        text_font = ImageFont.truetype(font_path, size= 12)
        text_color = get_color(values['-COLOR_SELECT-'])
        key_list = list(dicci.keys())
        number = 0

        print(text_color)
        for dicci in text_boxes_list:
            # Divide el texto en líneas de acuerdo con el ancho especificado
            lines = textwrap.wrap(key_list[number], width= int(dicci[key_list[number]][2] // 6)) #ajusta cada linea al ancho del rectangulo, esto retorna una lista

            #Calcula la altura total necesaria para todas las líneas de texto
            total_height = len(lines) * draw.textsize('A', font= text_font)[1] #calcula el tamaño del texto usando "A" como referncia.
            #se genera una tupla con ancho y altura, que se obtiene con [1]

            if total_height <= (dicci[key_list[number]][3] - dicci[key_list[number]][1]):
                # Hay suficiente espacio vertical para mostrar todas las líneas
                draw.rectangle([dicci[key_list[number]][0], dicci[key_list[number]][1],
                                dicci[key_list[number]][2], dicci[key_list[number]][3]],
                                width= 0)

                # Dibuja cada línea de texto en posiciones verticales separadas
                for i, line in enumerate(lines):
                    line_y = dicci[key_list[number]][1] + (i * draw.textsize('A', font= text_font)[1])
                    draw.text((dicci[key_list[number]][0], line_y),
                              line,
                              font= text_font,
                              fill= text_color,
                              align= 'center')
            else:
                # No hay suficiente espacio vertical para mostrar todas las líneas,
                # se recorta el texto
                truncated_lines = lines[:int((dicci[key_list[number]][3] - dicci[key_list[number]][1]) // draw.textsize('A', font= text_font)[1])]
           
                truncated_text = '\n'.join(truncated_lines)
          
                draw.rectangle([dicci[key_list[number]][0], dicci[key_list[number]][1],
                                dicci[key_list[number]][2], dicci[key_list[number]][3]],
                                width= 0)
                
                draw.text(xy= (dicci[key_list[number]][0], dicci[key_list[number]][1]),
                          text= truncated_text,
                          font= text_font,
                          fill= text_color,
                          align= 'center')

            number += 1
        
        photo_img = ImageTk.PhotoImage(image)
        window['-IMAGE-'].update(data= photo_img)        

    return image


def create_window(img_data):
    """
    Crea los elementos del layout y la ventana.

    Returns
    -------
        PySimpleGUI.Window
    """
    font_select_text = sg.Text(text= 'Seleccionar Fuente: ')

    font_list = ['AdobeVF Prototype', 'Aref Ruqaa',
                 'FreeMono', 'Noto Sans']
    font_dropdown = sg.Combo(key= '-FONT_SELECT-',
                             values= font_list,
                             default_value= 'AdobeVF Prototype',
                             size= (18, 1),
                             readonly= True)


    color_select_text = sg.Text(text= 'Seleccionar Color: ')

    color_list = ['Negro', 'Blanco', 'Rojo', 'Azul', 'Amarillo',
                  'Verde', 'Violeta', 'Naranja', 'Rosa', 'Marrón']
    color_dropdown = sg.Combo(key= '-COLOR_SELECT-',
                              values= color_list,
                              default_value= 'Negro',
                              size= (15, 1),
                              readonly= True)


    meme_text_list = []
    number = 0
    for dicci in img_data['text_boxes']:
        text_title = sg.Text(key= '-TEXT_TITLE_' + str(number + 1) + '-',
                         text= 'Texto ' + str(number + 1))
    
        text_input = sg.Multiline(key= '-TEXT_INPUT_' + str(number + 1) + '-',
                              size= (14, 2))
        
        #print(int(number / 2))

        if(len(meme_text_list) > 0) and (number % 2) != 0:
            meme_text_list[int(number / 2)].append(text_title)
            meme_text_list[int(number / 2)].append(text_input)    
        
        else:
            box = [text_title, text_input]        
            meme_text_list.append(box)
        
        number += 1


    update_button = sg.Button(key= '-UPDATE_BUTTON-',
                              button_text= 'Aplicar Cambios')

    config_path = os.path.join(DIR_PROYECTO, 'data', 'config.json')

    img_path = ''
    try:            
        with open(config_path, encoding= 'utf-8', mode = "r") as config_file:            
            config_data = json.load(config_file)
            
            img_path = os.path.join(DIR_PROYECTO, config_data['imagenes'], img_data['image'])

    except FileNotFoundError:
        sg.PopupOK('No se encuentra el template seleccionado...\nPor favor, verifique que las rutas en el menú de Configuración sean correctas.')

    image = sg.Image(key= '-IMAGE-',
                     filename= img_path)

    horizontal_sep_1 = sg.HorizontalSeparator(key= '-HOR_SEP_1-')
    horizontal_sep_2 = sg.HorizontalSeparator(key= '-HOR_SEP_2-')

    back_button = sg.Button(key= '-BACK_BUTTON-',
                          button_text= 'Volver',
                          button_color= ('White', 'Red'))
    
    save_button = sg.Button(key= '-SAVE_BUTTON-',
                           button_text= 'Guardar Imagen')
 
 
    layout = [[font_select_text, font_dropdown],
            [color_select_text, color_dropdown],
            [horizontal_sep_1],
            meme_text_list,
            [update_button],
            [image],
            [horizontal_sep_2],
            [back_button, save_button]]

  
    window = sg.Window("Generar Meme - UNLPImage",
                       layout,
                       margins=(15,30))
    
    return window


def generador_memes(user_Data, my_template):
    """
    Ejecuta y muestra en pantalla la ventana y maneja los eventos de la misma.

    Parameters
    ----------
    user_Data: dict
        Diccionario con los datos de un único usuario.
    my_template: str
        Nombre de la plantilla a usar para el meme.
    """
    img_data = get_image_data(my_template)
    my_window = create_window(img_data)
    
    nick_List = list(user_Data.keys())
    current_User = nick_List[0]
    
    my_meme = None

    while True:
        event, values = my_window.read()
        print(f'Evento: {event}; Valores: {values}')

        match event:
            case '-UPDATE_BUTTON-':
                image_path = os.path.join(DIR_PROYECTO, 'imagenes', img_data['image'])
                image = Image.open(image_path)
                my_meme = apply_text(image, img_data['text_boxes'], values, my_window)

            case '-SAVE_BUTTON-':
                meme_texts = ''
                number = 1

                if my_meme is not None: 
                    for dicci in img_data['text_boxes']:
                        meme_texts += values[f'-TEXT_INPUT_{str(number)}-'] + ';'
                        number += 1

                    save_image(my_meme, my_template, current_User, img_data['image'], meme_texts)
                else:
                    sg.PopupOK("Por favor aplique los cambios antes de guardar") 
            case '-BACK_BUTTON-':
                user_Confirm = sg.PopupYesNo('¿Volver a la pantalla de selección de template?')
                if(user_Confirm == 'Yes'):
                    my_window.hide()
                    memes.selector_memes(user_Data)
                    break

            case sg.WIN_CLOSED:
                break

    my_window.close()

if __name__== '__main__':
    generador_memes()