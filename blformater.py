import re
import logging

VERSION = '0.3' # control de version

#--------Lista de variables--------
#--------Nombre del archivo que se va a genera. Puedes usar formato .txt
FILE_NAME = "blacklist.rsc"
#--------Nombre del archivo de logs
LOG_FILE_NAME = "lists.log"
#--------Cuantos archivos de listas hay en el directorio actual.
NUMBER_OF_FILES = 5
#--------Cadena que se agregara antes del dominio.
PRE_STRING = "/ip firewall address-list add list=blacklist address="
#--------Cadena agregada despues del dominio
POST_STRING = ";"

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename=LOG_FILE_NAME,\
                    level=logging.DEBUG,\
                    format=LOG_FORMAT)
logger = logging.getLogger()

#Patrones de busqueda para correccion de dominios
SEARCH_PATTERN = { 
    "HAS_HTTP": re.compile(r"(?:^http:\/\/)([a-z0-9.]*)"),
    "HAS_WWW": re.compile(r"((?:w{3}\.)([a-z.]*))"),
    "HAS_IP_AND_PORT": re.compile(r"((?:w{3}\.)?(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}))"),
    "DOMAIN_ONLY": re.compile(r"[a-z0-9.-]*"),
}

#Patrones de busqueda para eliminar lineas
DELETE_PATTERN = { 
    "BLANK_LINE": re.compile("^$"),
    "BEGIN_ALPHABETICAL": re.compile("^[a-zA-Z]"),
}

#Funcion para leer un archivo y filtar las lineas que no se necesitan
def readDomains(file_name):
    lista = ""
    line_number = 0
    try:
        logger.info(f"Abriendo archivo {file_name}")
        file_open =  open(file_name, "r")
        logger.info(f"Leyendo archivo {file_name}")
        for linea in file_open.readlines():
            line_number += 1
            if linea == '\n':
                logger.debug(f"Omitida linea {line_number} Rason: Linea vacia")
                pass
            elif not DELETE_PATTERN["BEGIN_ALPHABETICAL"].match(linea):
                logger.debug(f"Omitida linea {line_number} Rason: no es un dominio")
                pass
            else:
                lista += linea
    except:
        logger.error(f"Omitiendo archivo {file_name} Rason: no encontrado")
        return lista
    else:
        logger.info(f"Archivo {file_name} leido con exito")
        return lista


#Funcion para que se inicie la lectura de todos los archivos con listas negras
def readFiles():
    listas = ""
    for i in range(NUMBER_OF_FILES):
        listas += readDomains(f"{i+1}.txt")
    return listas.split('\n')
    
#Funcion principal (el programa)
def main():
    logging.info("Iniciando el scritp")
    listfile = readFiles()
    blacklist = ""
    cache = []

    for line in listfile:
        #Filtrado de los dominios para que esten bien escritos
        has_www = SEARCH_PATTERN["HAS_WWW"].match(line)
        has_http = SEARCH_PATTERN["HAS_HTTP"].match(line)
        has_ip = SEARCH_PATTERN["HAS_IP_AND_PORT"].match(line)
        domain_only = SEARCH_PATTERN["DOMAIN_ONLY"].match(line)
        new_line = ""

        if has_ip:
            new_line =  f"{PRE_STRING}{has_ip[1]}{POST_STRING}\n"
            logger.debug(f"Cambio {line} > {has_ip[1]}")
        elif has_www:
            new_line =  f"{PRE_STRING}{has_www[0]}{POST_STRING}\n"
            logger.debug(f"Cambio {line} > {has_www[0]}")
        elif has_http:
            new_line =  f"{PRE_STRING}{has_http[1]}{POST_STRING}\n"
            logger.debug(f"Cambio {line} > {has_http[1]}")
        elif line == '':
            pass
        else:
            new_line =  f"{PRE_STRING}{domain_only[0]}{POST_STRING}\n"

        # verifica que la linea no este repetida
        if new_line not in cache:
            blacklist += new_line
            logger.debug(f"Dominio agregado: {new_line}")
            cache.append(new_line)
    
    with open(FILE_NAME, "w") as file:
        logger.info(f"Escribiendo en archivo {FILE_NAME}")
        file.writelines(blacklist[:-1])
        logger.info(f"Escritura finalizada")
        
if __name__ == '__main__':
    main()
