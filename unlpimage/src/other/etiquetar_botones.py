import os
import datetime
import src.other.manejador_csv as csv_handler
import PySimpleGUI as sg
from PIL import Image
import mimetypes
import src.paths as paths
from src.paths import DIR_PROYECTO


def load_tags(tag_list):
    """
    Obtiene los Tags que están guardados actualmente en la lista de Tags.

    Parameters
    ----------
    tag_list: list
            Lista con los Tags de la imagen actual.

    Returns
    -------
        str
    """
    tags = ''
    for tag in tag_list:
        tags += f'{tag}; '
    return tags


def back():
    """
    Solicita confirmación sobre si el usuario quiere o no volver al menú principal.

    Returns
    -------
        str
    """
    confirmation = sg.PopupYesNo('¿Volver al menú principal?\nSe perderán los cambios sin guardar.')
    return confirmation


def tag(window, tag, tag_list, real_path):
    """
        Agrega Tag a la lista de Tags para la imagen actual.

        Parameters
        ----------
        window: PySimpleGUI.Window
            Ventana que se está ejecutando actualmente.
        tag: str
            Tag que se desea agregar a la lista de Tags de la imagen.
        tag_list: list
            Lista con los Tags de la imagen actual.
        real_Path: boolean
            Boolean para corroborar que realmente haya una imagen cargada.
        
        Returns
        -------
            list
    """
    if real_path:
        if tag and not tag.isspace():
            if (len(tag_list) < 5):

                if tag not in tag_list:
                    tag_list.append(tag.upper())    
                    window['-TAG_LIST-'].update(f'{load_tags(tag_list)}')

                else:
                    sg.PopupOK(f'El Tag "{tag}" ya existe para esta imagen.')
            else:
                sg.PopupOK('Se ingresaron demasiados Tags para esta imagen.\nPor favor, borre un Tag antes de ingresar uno nuevo.')
        else:
            sg.PopupOK('No se ingresó ningún Tag.\nPor favor, vuelva a intentarlo.')
    else:
        sg.PopupOK('Por favor, cargue una imagen antes de ingresar un Tag.')

    return tag_list

def description(window, new_desc, desc_string, real_path):
    """
        Agrega una descripción para la imagen actual.

        Parameters
        ----------
        window: PySimpleGUI.Window
            Ventana que se está ejecutando actualmente.
        new_desc: string
            Descripción que se desea agregar a la imagen.
        desc_string: str
            Descripción actual de la imagen.
        real_Path: boolean
            Boolean para corroborar que realmente haya una imagen cargada.
        
        Returns
        -------
            str
    """
    if real_path:
        if new_desc and not new_desc.isspace():
            window['-DESCRIPTION-'].update(new_desc)
            return new_desc
        else:
            sg.PopupOK('No se ingresó ninguna Descripción.\nPor favor, vuelva a intentarlo.')
            return desc_string
    else:
        sg.PopupOK('Por favor, cargue una imagen antes de ingresar una descripción.')
        return desc_string


def tag_delete(window, tag_list, real_path):
    """
        Borra un Tag de la lista de Tags actuales.

        Parameters
        ----------
        window: PySimpleGUI.Window
            Ventana que se está ejecutando actualmente.
        tag_list: list
            Lista con los tags de la imagen actual.
        real_Path: boolean
            Boolean para corroborar que realmente haya una imagen cargada.
        
        Returns
        -------
            list
        
        Raises
        ------
            ValueError
    """
    if real_path:
        tag = sg.PopupGetText(title= 'Borrar un Tag - UNLPImage',
                              message= 'Ingrese el Tag que desea borrar:')
        if tag is not None:    
            confirmation = sg.PopupYesNo(f'¿Está seguro que desea borrar el Tag "{tag.upper()}"?')
        
            if confirmation == 'Yes':
                try:
                    tag_list.remove(tag.upper())
                    window['-TAG_LIST-'].update(f'{load_tags(tag_list)}')

                except ValueError:
                    sg.PopupError('El Tag ingresado no existe para esta imagen.',
                                title= 'Error - UNLPImage')
                except:
                    sg.PopupError('Ocurrió un error inesperado.\nPor favor, vuelva a intentarlo.',
                                  title= 'Error - UNLPImage')    
        else:
            sg.PopupOK('No se ingresó ningún Tag.\nPor favor, vuelva a intentarlo.')    
    else:
        sg.PopupOK('Por favor, cargue una imagen antes de realizar esta acción.')

    return tag_list


def desc_delete(window, real_path):
    """
        Borra la Descripción actual.

        Parameters
        ----------
        window: PySimpleGUI.Window
            Ventana que se está ejecutando actualmente
        real_Path: boolean
            Boolean para corroborar que realmente haya una imagen cargada.
        
        Returns
        -------
            str
    """
    if real_path:
        confirmation = sg.PopupYesNo('¿Está seguro que desea borrar la descripción de la imagen?')
    
        if confirmation == 'Yes':
            window['-DESCRIPTION-'].update('')
            return ''

    else:
        sg.PopupOK('Por favor, cargue una imagen antes de realizar esta acción.')
        return ''


def load_image(window, data_list, tag_list, desc_string, img_path, real_path):
    """
        Muestra la imagen de la ruta que se seleccionó en pantalla, junto con sus respectivos datos.
        Si es una nueva imagen, carga los datos de su metadata. Sino, carga sus datos de un archivo '.csv'.
        
        Parameters
        ----------
        window: PySimpleGUI.Window
            Ventana que se está ejecutando actualmente.
        data_list: list
            Lista que contiene datos sobre la imagen actual.
        tag_list: list
            Lista con los tags de la imagen actual.
        desc_string: str
            String con la descripción de la imagen actual.
        img_Path: string
            String que contiene la ruta de la imagen que se desea mostrar.
        real_path: boolean
            Boolean para corroborar que realmente haya una imagen cargada.

        Returns
        -------
            str, list, list, boolean

        Raises
        ------
            AttributeError
            FileNotFoundError
            PIL.Image.UnidentifiedImageError
    """
    try:
        data_list = csv_handler.load_data(img_path)
        print(data_list, paths.convertir_guardado_para_usar(img_path, DIR_PROYECTO))

        if len(data_list) == 0:
        
            img = Image.open(img_path)

            img_path_list = os.path.split(img_path)

            img_type = mimetypes.guess_type(img_path)

            img_size = os.path.getsize(img_path) * 0.001
        
            img_date = datetime.datetime.fromtimestamp(os.path.getctime(img_path)).strftime(f'Fecha y Hora de Creación: %d/%m/%Y, %H:%M:%S, %A')
            img_res = f'{img.width} x {img.height}'

            window['-IMG_NAME-'].update(f'Nombre: {img_path_list[1]}')
            window['-IMG-'].update(img_path)
            window['-IMG_MIMETYPE-'].update(f'Tipo: {img_type[0]}')
            window['-IMG_SIZE-'].update(f'Tamaño: {img_size} KB')
            window['-IMG_RES-'].update(f'Resolución: {img_res}')
            window['-IMG_DATE-'].update(img_date)
            window['-TAG_LIST-'].update('')
            window['-DESCRIPTION-'].update('')

            desc_string = ''
            tag_list.clear()

            my_data = [paths.convertir_para_guardar(img_path, DIR_PROYECTO),
                       desc_string, img_res, img_size,
                       img_type[0], tag_list]

            for elem in my_data:
                data_list.append(elem)    

            print(f'Nuevo: {data_list}')

        else:
            my_path = paths.convertir_guardado_para_usar(data_list[0], DIR_PROYECTO)

            img = Image.open(my_path)

            img_path_list = os.path.split(data_list[0])

            img_type = data_list[4]

            img_size = data_list[3]
        
            img_date = datetime.datetime.fromtimestamp(os.path.getctime(data_list[0])).strftime(f'Fecha y Hora de Creación: %d/%m/%Y, %H:%M:%S, %A')
            img_res = data_list[2]

            desc_string = data_list[1]
            tag_list.clear()
            my_tags_a = data_list[5].replace('[', '')
            my_tags_b = my_tags_a.replace(']', '')
            my_tags_c = my_tags_b.replace("'", "")
            my_tags_d = my_tags_c.replace(' ', '')
            my_tags_list = my_tags_d.split(',')
            for tag in my_tags_list:
                print(tag)
                tag_list.append(tag)
                print(f'MIS TAGSAOFW {tag_list}')
                

            window['-IMG_NAME-'].update(f'Nombre: {img_path_list[1]}')
            window['-IMG-'].update(data_list[0])
            window['-IMG_MIMETYPE-'].update(f'Tipo: {img_type[0]}')
            window['-IMG_SIZE-'].update(f'Tamaño: {img_size} KB')
            window['-IMG_RES-'].update(f'Resolución: {img_res}')
            window['-IMG_DATE-'].update(img_date)
            window['-TAG_LIST-'].update(load_tags(tag_list))
            window['-DESCRIPTION-'].update(desc_string)

            print(f'Existe: {data_list}\n{desc_string}')

        real_path = True
        return desc_string, data_list, tag_list, real_path
    
    except AttributeError:
        sg.PopupError('No se especificó ninguna ruta.\nPor favor vuelva a intentarlo.',
                        title= 'Error - UNLPImage')
        return '', [], [], False

    except FileNotFoundError:
        sg.PopupError('No se encontró ningún archivo.\nPor favor, verifique que la ruta ingresada sea correcta.',
                    title= 'Error - UNLPImage')
        return '', [], [], False

    except Image.UnidentifiedImageError:
        sg.PopupError('La ruta del archivo ingresada no corresponde a una imagen.\nPor favor, vuelva a intentarlo.',
                    title= 'Error - UNLPImage')
        return '', [], [], False


def save(user, data_list, tag_list, desc_string):
    """
        Agrega a la lista de datos la descripción y la lista de Tags.
        Luego llama a una función encargada de realizar el guardado de los datos.

        Parameters
        ----------
        user: string
            El nombre del usuario actual.
        data_list: list
            Lista que contiene datos sobre la imagen actual.
        tag_list: list
            Lista con los tags de la imagen actual.
        desc_string: str
            String con la descripción de la imagen actual.
    """
    
    data_list[1] = desc_string
    data_list[5] = tag_list

    csv_handler.save_data(data_list, user)
    sg.PopupOK('Los cambios se guardaron con éxito.')
