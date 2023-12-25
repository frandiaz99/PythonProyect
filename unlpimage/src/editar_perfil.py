import PySimpleGUI as sg
import os
import src.other.funciones_editar as funciones
import src.menu_principal as menu 
from src.paths import DIR_PROYECTO
    
def crear_window(nick,dicci,gen,avat):    
    """
        Se crea los layout con los datos del perfil con el cual se accedio 
        al editar perfil.
    
        Parameters
        ----------
        nick: str
            Nick del usuario del perfil actual.
        dicci: dict
            Diccionario con la informacion referente al usuario.
        gen: str
            Genero que se va a actualizar y utilizar. 
        avat: str
            Avatar del perfil.
        
        Returns
        -------
            PySimpleGUI.Window
    """
    
    avatar_path= os.path.join(DIR_PROYECTO,'avatar')
    lista_generos= ['mujer', 'hombre', 'no binario']
    nom= dicci[nick]["NOMBRE"]
    edad= dicci[nick]["EDAD"]
    gen= dicci[nick]["GENERO"]
    prendido=False
    str_gen=''
    
    if (gen!='hombre') and (gen != 'mujer') and (gen != 'no binario'):
        prendido=True
        str_gen=gen

    boton_volver=sg.Button("Volver", key="-VOLVER-",size=(13,2), pad=(0,20))
    boton_guardar= sg.Button("Guardar Cambios", key="-GUARDAR_CAMBIOS-",size=(13,2), pad=(0,20))
 
    col_layout_uno=[
        [sg.Text('NICK: '),sg.Text(key='-NICK-',pad=(15,5),text=nick)],
        [sg.Text(' ingresa un nuevo nombre: ')],
        [sg.InputText(key='-NOMBRE-',default_text=(nom))],
        [sg.Text('ingresa la edad: ')], 
        [sg.Input(edad,key='-EDAD-')],
        [sg.Text('cambiar genero autopercibido: ')],
        [sg.Listbox(lista_generos, key='-GENERO_LISTADO-', expand_y=True, size=(10, 5), select_mode='single',default_values=gen)],
        [sg.Checkbox('otro',key='-OTRO-',default=prendido)],
        [sg.InputText(key='-GENERO_INPUT-',default_text=(str_gen))]
    ]

    col_layout_dos=[
        [sg.Image(avat,key='-AVATAR_POR_DEFECTO-')],
        [sg.FileBrowse('seleccionar nuevo Avatar ', key='-AVATAR-',pad=(1,20), initial_folder=avatar_path)],
        [sg.Button("Actualizar Avatar", key="-EDI_AVATAR-")]   
    ]
    
    layout = [
        [sg.Text(' '*135),boton_volver],
        [sg.Column(col_layout_uno),sg.Text(' '*10), sg.Column(col_layout_dos)],
        [sg.Text(' '*135), boton_guardar]
    ]

    editar_window = sg.Window("EDITAR PERFIL", layout, margins=(15,30))
    return editar_window

def editar_perfil(dicci):
    """
        se ejecuta laventana editar perfil y se actuliza con los nuevos 
        datos ingresados por teclado.
        
        Parameters
        ----------
        dicci: dict
            Diccionario con la informacion referente al usuario.
        
    """
           
    nick_List = list(dicci.keys())
    nick= nick_List[0]
    avat= dicci[nick]["AVATAR"]
    gen= ''
    window=crear_window(nick,dicci,gen,avat)

    while True:
        event, values = window.read()
        if (event == sg.WIN_CLOSED):
            break
        print(f"provar1, Evento: {event}, valores: {values}")
        
        valores= dict([('NOMBRE', values['-NOMBRE-']), ('EDAD', values['-EDAD-']), ('GENERO', funciones.genero(values,gen)), ('AVATAR', funciones.edi_avatar(values,avat))])
        print(f"prova2, Evento: {event}, valores: {values}")        
        dicci[nick]=valores

        match event:
            case '-EDI_AVATAR-':
                if(values['-AVATAR-'] != ""):
                    window['-AVATAR_POR_DEFECTO-'].update(values['-AVATAR-'])
            case '-VOLVER-':
                window.hide() 
                if(funciones.validar_valores(dicci)):
                    menu.menu_principal(dicci)                
                break            
            case '-GUARDAR_CAMBIOS-':
                if(funciones.validar_valores(dicci)):
                    funciones.guardar_cambios(nick,valores)

        if (event == sg.WIN_CLOSED):
            break        

    window.close()

if __name__== '__main__':
    editar_perfil()     