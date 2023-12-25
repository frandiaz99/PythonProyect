import os.path 

DIR_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


#path del proyecto 
print (f"DIR_PROYECTO: {DIR_PROYECTO}")


def convertir_para_guardar (path, path_proyecto): 
    """
    convierte la ruta recibida a una relativa y en el formato de linux

    Parameters
    ----------
    path: str
        path a convertir 
    path_proyecto: str
        ruta del archivo raiz 'unlpimage.py'
    
    Returns
    --------
        str
    """
    #el parametro path proyecto va a ser la constante DIR_PROYECTO

    #calculo el path relativo
    path_relativo=os.path.relpath(path, start=path_proyecto)
    #convierto el path relativo a un path de linux 
    path_generico= path_relativo.replace(os.path.sep, "/")

    return path_generico


def convertir_guardado_para_usar(path, path_proyecto): 
    """
    convierte una ruta relativa en formato de linux en una abosluta y en el formato del sistema operativo 
    en el cual se esta ejecutando el programa 

    Parameters
    ----------
    path: str
        ruta relativa a convertir
    path_proyecto: str
        ruta del archivo raiz 'unlpimage.py'

    Returns
    -------
        str
    """
    #me covierte un path guardado en uno que pueda usar en mi sistema opertivo
    path_del_sistema =path.replace("/", os.path.sep)
        

    path_absoluto = os.path.abspath(os.path.join(path_proyecto, path_del_sistema))
        
 
    return path_absoluto 


