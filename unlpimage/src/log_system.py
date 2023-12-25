import os
import csv
import datetime
from src.paths import DIR_PROYECTO
from datetime import datetime


def log_system(usuario, operacion, valores=None, textos=None):
    """
        Creacion o apertura de archivo csv.

        Parameters
        ----------
        Usuario: String
            Nick del usuario
        Operacion: String
            Operacion que realizo el usuario
        valores: String
            Nombre de las imagenes usadas
        Texto: String
            Textos usados en la imagen.
    """

    log_path = os.path.join(DIR_PROYECTO, 'data', 'log_system.csv')

    if not os.path.isfile(log_path):

        with open(log_path, mode="w", newline="") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(["Fecha", "Nombre Usuario",
                            "Operacion", "Valores", "Textos"])

    with open(log_path, mode="a", newline="") as archivo:

        writer = csv.writer(archivo)
        #fecha = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S, %A")
        fecha = datetime.timestamp(datetime.now())
        print(fecha)

        if (valores is None) and (textos is None):
            writer.writerow([fecha, usuario, operacion])
        else:
            writer.writerow([fecha, usuario, operacion, valores, textos])
