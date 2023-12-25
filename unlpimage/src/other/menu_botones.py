import PySimpleGUI as sg


def help():
    """
    Muestra en pantalla un Popup con información sobre ayuda y uso del programa.
    """
    help_list = ['Seleccione una de las siguientes opciones para comenzar a trabajar con UNLPImage:\n\n',
                '-ETIQUETAR IMAGENES-\n',
                'Usted podrá seleccionar una imagen de su computadora y aplicarle una o más etiquetas personalizadas a esta.\n',
                '-GENERAR MEME-\n',
                'Esta función le permitirá crear un meme personalizado a partir de una imagen a elección.\n',
                '-GENERAR COLLAGE-\n',
                'Con esta herramienta, usted podrá seleccionar una o más imágenes y modificar distintos aspectos de las mismas para crear una nueva imagen a partir de estas.\n',
                '-SALIR-\n',
                'Permite cerrar la sesión actual.\n',
                '-EDITAR PERFIL-\n',
                'Aquí podrá cambiar los datos acerca de su usuario de UNLPImage.\n',
                '-CONFIGURACION-\n',
                'Aquí podrá modificar la ruta de los distintos directorios con los que trabaja UNLPImage.']
    
    help_text = ""
    for elem in help_list:
        help_text += elem

    sg.PopupOK(help_text, title= 'Ayuda - UNLPImage')

def salir():
    """
    Solicita confirmación sobre si el usuario quiere o no cerrar la sesión actual.

    Returns
    -------
        string
    """
    confirmation = sg.PopupYesNo('¿Realmente quiere cerrar sesión?')
    return confirmation