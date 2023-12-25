import PySimpleGUI as sg
import os
import json
from PIL import Image
import src.other.etiquetar_botones as buttons
import src.menu_principal as menu
from src.paths import DIR_PROYECTO


def get_imagenes_path():
    """
    Accede a un archivo de configuración '.json' para obtener la ruta del repositorio de imagenes.
    
    Returns
    -------
        string
    """
    config_path = os.path.join(DIR_PROYECTO, 'data', 'config.json')
    my_imagenes_path = ''
    
    try:
        with open(config_path, 'r') as json_file:
            config_data = json.load(json_file)
            my_imagenes_path = os.path.join(DIR_PROYECTO, config_data['imagenes'])
    
    except FileNotFoundError:
        sg.PopupOK('La ruta del repositorio de imágenes no está bien configurada...\nPor favor, verifique que las rutas en el menú de Configuración sean correctas.')

    return my_imagenes_path

def create_window():
    """
    Crea los elementos del layout y la ventana.

    Returns
    -------
        PySimpleGUI.Window
    """
    imagenes_path = get_imagenes_path()

    back_button = sg.Button(key= '-VOLVER-',
                            button_text= '< Volver',
                            button_color= ('White', 'Red'))


    img_path = sg.InputText(key= '-IMG_PATH-')

    browse_button = sg.FileBrowse(key= '-BROWSE-',
                                  target= '-IMG_PATH-',
                                  button_text= 'Buscar Imagen',
                                  initial_folder= imagenes_path)

    load_button = sg.Button(key= '-LOAD_IMG-',
                            button_text= 'Cargar Imagen')

    tag_title = sg.Text('Tag')

    tag_input = sg.InputText(key= '-TAG_INPUT-',
                             do_not_clear= False)

    tag_button = sg.Button(key= '-TAG_BUTTON-',
                           button_text= 'Agregar')


    desc_title = sg.Text('Descripción')

    desc_input = sg.InputText(key= '-DESC_INPUT-',
                              do_not_clear= False)

    desc_button = sg.Button(key= '-DESC_BUTTON-',
                           button_text= 'Agregar')


    tag_layout = [sg.Text(' ' * 2), tag_input, tag_button]

    desc_layout = [sg.Text(' ' * 2), desc_input, desc_button]


    horizontal_sep_0 = sg.HorizontalSeparator(key= '-HOR_SEPARATOR_0-',
                                            pad= None)
    
    horizontal_sep_1 = sg.HorizontalSeparator(key= '-HOR_SEPARATOR_1-',
                                            pad= None)
    
    
    image_name = sg.Text(key= '-IMG_NAME-',
                         text_color= 'White')

    image = sg.Image(key= '-IMG-')    
    
    image_mimetype = sg.Text(key= '-IMG_MIMETYPE-')

    image_size = sg.Text(key= '-IMG_SIZE-')

    image_res = sg.Text(key= '-IMG_RES-')

    image_date = sg.Text(key= '-IMG_DATE-')

    vertical_sep_0 = sg.VerticalSeparator(key= '-VER_SEPARATOR_0-',
                                        pad= None)
    
    vertical_sep_1 = sg.VerticalSeparator(key= '-VER_SEPARATOR_1-',
                                        pad= None)


    tag_text = sg.Text(key= '-TAG_LIST-',
                       text_color= 'Red')
    
    desc_text = sg.Text(key= '-DESCRIPTION-',
                        text_color= 'Dark Blue')
    
    del_tag = sg.Button(key= '-TAG_DELETE-',
                        button_text= 'Borrar un Tag',
                        button_color= ('White', 'Red'))

    del_desc = sg.Button(key= '-DESC_DELETE-',
                        button_text= 'Borrar Descripción',
                        button_color= ('White', 'Red'))
    

    save_button = sg.Button(key= '-SAVE-',
                            button_text= 'Guardar',
                            button_color= ('Black', 'White'))
    
    etiquetar_layout = [[img_path, browse_button],
                        [load_button],                        
                        [horizontal_sep_0],
                        [image_name],
                        [image],
                        [image_mimetype, vertical_sep_0, image_size, vertical_sep_1, image_res],
                        [image_date],
                        [sg.Text(text= 'TAGS: ', text_color= 'Red'), tag_text],
                        [sg.Text(text= 'DESCRPICION: ', text_color= 'Dark Blue'), desc_text],         
                        [horizontal_sep_1],
                        [tag_title],
                        [tag_layout],
                        [desc_title],
                        [desc_layout],
                        [del_tag, del_desc, sg.Text(' ' * 20), back_button, save_button]]

    menu_window = sg.Window('Etiquetar Imagenes - UNLPImage', etiquetar_layout)
    return menu_window

# Testing
def etiquetar_imagenes(user_data):
    """
    Ejecuta y muestra en pantalla la ventana y maneja los eventos de la misma.

    Parameters
    ----------
    user_Data: dict
        Diccionario con los datos de un único usuario.
    """
    nick_list = list(user_data.keys())
    current_user = nick_list[0]
    real_path = False

    desc_string = ''
    tag_list = []
    data_list = []

    window = create_window()
    while True:
        event, values = window.read()
        print(f'Evento: {event}; Valores: {values}')

        match event:
            case '-VOLVER-':
                confirmation = buttons.back()
                if confirmation == 'Yes':
                    window.hide()
                    menu.menu_principal(user_data)
                    break

            case '-LOAD_IMG-':
                path = values['-IMG_PATH-']
                desc_string, data_list, tag_list, real_path = buttons.load_image(window, data_list, tag_list, desc_string, path, real_path)
            
            case '-TAG_BUTTON-':
                path = values
                tag = values['-TAG_INPUT-']
                tag_list = buttons.tag(window, tag, tag_list, real_path)
            
            case '-DESC_BUTTON-':
                new_desc = values['-DESC_INPUT-']
                desc_string = buttons.description(window, new_desc, desc_string, real_path)
            
            case '-TAG_DELETE-':
                tag_list = buttons.tag_delete(window, tag_list, real_path)
            
            case '-DESC_DELETE-':
                desc_string = buttons.desc_delete(window, real_path)
            
            case '-SAVE-':
                if real_path:
                    confirmation = sg.PopupYesNo('¿Está seguro que desea guardar los cambios realizados para esta imagen?'
                                             +'\nSe sobreescribiran los Tags y Descripción antigüos...')
                    if confirmation == 'Yes':
                        buttons.save(current_user, data_list, tag_list, desc_string)
                
                else:
                    sg.PopupOK('Por favor, cargue una imagen antes de realizar esta acción.')
            
            case sg.WIN_CLOSED:
                break

    window.close()

if __name__ == '__main__':
    etiquetar_imagenes()