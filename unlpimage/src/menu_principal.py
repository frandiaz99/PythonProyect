import PySimpleGUI as sg
import os
import src.other.menu_botones as buttons
import src.editar_perfil as perfil
import src.configuracion as configuration
import src.etiquetar_imagenes as etiquetar
import src.selector_memes as meme
import src.diseño_collage as collage
import src.inicio as title_screen
import src.paths as paths
from src.paths import DIR_PROYECTO


def create_window(my_nick, my_avatar):    
    """
    Crea los elementos del layout y la ventana.

    Parameters
    ----------
    my_Nick: string
        El nombre de usuario.
    my_Avatar: string
        La ruta donde se encuentra guardada la imagen del avatar del usuario.

    Returns
    -------
        PySimpleGUI.Window
    """
    # Nick, Profile, Config and Help images.

    menu_nick = sg.Text(text= my_nick)

    menu_config = os.path.join(DIR_PROYECTO, 'img', 'config.png')

    menu_help = os.path.join(DIR_PROYECTO, 'img', 'help.png')


    # Main Menu Buttons.
    profile_button = sg.Button(key= '-PROFILE-',
                               button_text= '',
                               image_source= my_avatar,
                               size= (7, 3),
                               pad= (0, 0),
                               button_color= (sg.theme_background_color(),
                                              sg.theme_background_color()))

    config_button = sg.Button(key= '-CONFIG-',
                            button_text= '',
                              image_source=menu_config,
                              size= (7, 3),
                              pad= (0, 0),
                              button_color= (sg.theme_background_color(),
                                             sg.theme_background_color()))

    help_button = sg.Button(key= '-HELP-',
                            button_text= '',
                            image_source= menu_help,
                            size= (7, 3),
                            pad= (10, 0),
                            button_color= (sg.theme_background_color(),
                                           sg.theme_background_color()))


    etiquetar_button = sg.Button(key= '-ETIQUETAR-',
                                  button_text= 'Etiquetar Imagenes',
                                  pad= (225, 5),
                                  size= (15, 2),
                                  button_color= ('Black', 'Cyan'))

    meme_button = sg.Button(key= '-MEME-',
                                button_text= 'Generar Meme',
                                pad= (225, 5),
                                size= (15, 2),
                                button_color= ('Black', 'Cyan'))

    collage_button = sg.Button(key= '-COLLAGE-',
                                button_text= 'Generar Collage',
                                pad= (225, 5),
                                size= (15, 2),
                                button_color= ('Black', 'Cyan'))

    salir_button = sg.Button(key= '-SALIR-',
                                button_text= 'Salir',
                                pad= (225, 5),
                                size= (15, 2),
                                button_color= ('Black', 'Orange'))


    # Window Layout.
    menu_layout = [[profile_button, sg.Text(' '*90), config_button, help_button],
                    [menu_nick],
                    [etiquetar_button],
                    [meme_button],
                    [collage_button],
                    [salir_button]]


    # Window Creation.
    menu_window = sg.Window('Menu Principal - UNLPImage', menu_layout,
                            metadata={'perfil_actual': None})
    return menu_window


# Testing.
def menu_principal(user_data):
    """
    Ejecuta y muestra en pantalla la ventana y maneja los eventos de la misma.

    Parameters
    ----------
    user_Data: dict
        Diccionario con los datos de un único usuario.
    """
    nick_list = list(user_data.keys())
    print(nick_list)
    window = create_window(nick_list[0], user_data[nick_list[0]]['AVATAR'])

    while True:
        event, values = window.read()
        print(f'Evento: {event}; Valores: {values}')

        match event:        
            case '-PROFILE-':
                window.hide()
                perfil.editar_perfil(user_data)
                break
            case '-CONFIG-':
                window.hide()
                configuration.configuracion(user_data)
                break
            case '-HELP-':
                buttons.help()
            case '-ETIQUETAR-':               
                window.hide() 
                etiquetar.etiquetar_imagenes(user_data)                
                break
            case '-MEME-':
                window.hide()
                meme.selector_memes(user_data)
                break
            case '-COLLAGE-':
                window.hide()
                collage.diseño_collage(user_data)
                break
            case '-SALIR-':
                user_confirm = buttons.salir()
                if(user_confirm == 'Yes'):
                    window.hide()
                    title_screen.inicio()
                    break
            case sg.WIN_CLOSED:
                break

    window.close()

if __name__ == '__main__':   
    menu_principal()