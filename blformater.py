'''
Codigo para formatear listas negras de dominios para Mikrotik
'''
import re
import logging

VERSION = "0.4"  # control de version

# --------Lista de variables--------
# --------Nombre del archivo que se va a genera. Puedes usar formato .txt
FILE_NAME = "blacklist.rsc"
# --------Nombre del archivo de logs
LOG_FILE_NAME = "lists.log"
# --------Cuantos archivos de listas hay en el directorio actual.
NUMBER_OF_FILES = 5
# --------Cadena que se agregara antes del dominio.
PRE_STRING = "/ip firewall address-list add list=blacklist address="
# --------Cadena agregada despues del dominio
POST_STRING = ";"

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename=LOG_FILE_NAME, level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()

# Patrones de busqueda para correccion de dominios
SEARCH_PATTERN = {
    "HAS_HTTP": re.compile(r"(?:^http:\/\/)([a-z0-9.]*)"),
    "HAS_WWW": re.compile(r"((?:w{3}\.)([a-z.]*))"),
    "HAS_IP_AND_PORT": re.compile(r"((?:w{3}\.)?(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}))"),
    "DOMAIN_ONLY": re.compile(r"[a-z0-9.-]*"),
}

# Patrones de busqueda para eliminar lineas
DELETE_PATTERN = {
    "BLANK_LINE": re.compile("^$"),
    "BEGIN_ALPHABETICAL": re.compile("^[a-zA-Z]"),
}

# Funcion para leer un archivo y filtar las lineas que no se necesitan
def read_domains(file_name):
    '''
    Funcion para leer un archivo y filtar las lineas que no se necesitan
    '''
    lista = ""
    line_number = 0
    try:
        logger.info("Abriendo archivo %s", file_name)
        with open(file_name, "r", encoding="utf-8") as file_open:
            logger.info("Leyendo archivo %s", file_name)
            for linea in file_open.readlines():
                line_number += 1
                if linea == '\n':
                    logger.debug("Omitida linea %s Rason: Linea vacia", line_number)
                elif not DELETE_PATTERN["BEGIN_ALPHABETICAL"].match(linea):
                    logger.debug("Omitida linea %s Rason: no es un dominio", line_number)
                else:
                    lista += linea
    except FileNotFoundError:
        logger.error("Omitiendo archivo %s Rason: no encontrado", file_name)
        return lista

    logger.info("Archivo %s leido con exito", file_name)
    return lista


# Funcion para que se inicie la lectura de todos los archivos con listas negras
def read_files():
    '''
    Funcion para que se inicie la lectura de todos los archivos con listas negras
    '''
    listas = ""
    for i in range(NUMBER_OF_FILES):
        listas += read_domains(f"{i+1}.txt")
    return listas.split('\n')


# Funcion principal (el programa)
def main():
    '''
    Funcion principal
    '''
    logging.info("Iniciando el scritp")
    listfile = read_files()
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
            new_line = f"{PRE_STRING}{has_ip[1]}{POST_STRING}\n"
            logger.debug("Cambio %s > %c", line, has_ip[1])
        elif has_www:
            new_line = f"{PRE_STRING}{has_www[0]}{POST_STRING}\n"
            logger.debug("Cambio %s > %c", line, has_www[1])
        elif has_http:
            new_line = f"{PRE_STRING}{has_http[1]}{POST_STRING}\n"
            logger.debug("Cambio %s > %c", line, has_http[1])
        elif line == '':
            pass
        else:
            new_line = f"{PRE_STRING}{domain_only[0]}{POST_STRING}\n"

        # verifica que la linea no este repetida
        if new_line not in cache:
            blacklist += new_line
            logger.debug("Dominio agregado: %s", new_line)
            cache.append(new_line)

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        logger.info("Escribiendo en archivo %s", FILE_NAME)
        file.writelines(blacklist[:-1])
        logger.info("Escritura finalizada")

if __name__ == '__main__':
    main()
