import os
from pathlib import Path
from time import strftime
import csv
import PySimpleGUI as sg
import src.log_system as logs
import src.paths as paths
from src.paths import DIR_PROYECTO


def load_data(img_path):
    """
        Lee un archivo '.csv' para obtener los datos de una imagen especifica.
        Si existen datos de la imagen, los agrega a una lista.

        Parameters
        ----------
        img_Path: str
            String que contiene la ruta de la imagen cuyos datos se desean obtener.

        Returns
        -------
            list    
        
        Raises
        ------
            FileNotFoundError
            ValueError
    """
    etiquetas_path = os.path.join(DIR_PROYECTO, 'data', 'etiquetas.csv')

    data_list = []

    try:
        with open(etiquetas_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
        
            for line in csv_reader:
                print(line[0])

                if line[0] == paths.convertir_para_guardar(img_path, DIR_PROYECTO):
                
                    for elem in line:
                        data_list.append(elem)
        
        return data_list
    
    except FileNotFoundError:
        return data_list
    except ValueError:
        sg.PopupError('No se encontró ningún archivo.\nPor favor, verifique que la ruta ingresada sea correcta.',
                    title= 'Error - UNLPImage')
        return data_list 



def save_data(data_list, user):
    """
        Escribe sobre archivo '.csv' los datos de una imagen especifica.
        Si no hay datos de la imagen en el archivo, los agrega como una nueva entrada.
        Sino, modifica los datos de la misma en el archivo.

        Parameters
        ----------
        data_List: list
            Lista que contiene los datos a guardar de la imagen.
        user: string
            String que contiene el nombre de usuario actual.
        
        Raises
        ------
            FileNotFoundError
    """
    etiquetas_path = os.path.join(DIR_PROYECTO, 'data', 'etiquetas.csv')

    try:
        line_list = []
        operation = ''

        with open(etiquetas_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ',')
        
            for line in csv_reader:                
                line_list.append(line)


        exists = False

        for line in line_list:            

            if line[0] == data_list[0]:
                
                if data_list[1] and ((data_list[1] != '') or (not data_list[1].isspace())):
                    line[1] = data_list[1]
                if data_list[5] and ((data_list[5] != '') or (not data_list[5].isspace())):
                    line[5] = data_list[5]
                
                line[6] = user
                current_time = strftime('%d/%m/%Y, %H:%M:%S, %A')
                line[7] = current_time

                exists = True
                operation = 'Modificación de imagen previamente clasificada'            

        if not exists:
            data_list.append(user)

            current_time = strftime('%d/%m/%Y, %H:%M:%S, %A')
            data_list.append(current_time)

            line_list.append(data_list)
            operation = 'Nueva imagen clasificada'
                
    
        with open(etiquetas_path, 'w', newline= '') as csv_file:
            csv_writer = csv.writer(csv_file)

            for line in line_list:
                print(line)
                csv_writer.writerow(line)
        
        logs.log_system(user, operation)
    
    except FileNotFoundError:
        with open(etiquetas_path, 'w', newline= '') as csv_file:
            csv_writer = csv.writer(csv_file)

            header = ['Ruta de la Imagen', 'Descripción',
                                'Resolución', 'Tamaño',
                                'Tipo', 'Lista de Tags',
                                'Último Perfil que Actualizo',
                                'Fecha de Última Actualización']
            

            csv_writer.writerow(header)
            
            data_list.append(user)

            current_time = strftime('%d/%m/%Y, %H:%M:%S, %A')
            data_list.append(current_time)

            csv_writer.writerow(data_list)

        logs.log_system(user, 'Nueva imagen clasificada')
    

