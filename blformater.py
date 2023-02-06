import re

#--------Lista de variables--------
#--------Cuantos archivos de listas hay en el directorio actual.
NUMBER_OF_FILES = 5
#--------Nombre del archivo que se va a genera. Puedes usar formato .txt
FILE_NAME = "blacklist.rsc"
#--------Cadena que se agregara antes del dominio.
PRE_STRING = "/ip firewall address-list add list=blacklist address="
#--------Cadena agregada despues del dominio
POST_STRING = ";"

#Patrones de busqueda para correccion de dominios
SEARCH_PATTERN = { 
    "HAS_HTTP": re.compile(r"(?:^http:\/\/)([a-z.]*)"),
    "HAS_WWW": re.compile(r"((?:w{3}\.)([a-z.]*))"),
    "HAS_IP_AND_PORT": re.compile(r"((?:w{3}\.)?(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}))"),
}

#Patrones de busqueda para eliminar lineas
DELETE_PATTERN = { 
    "BLANK_LINE": re.compile("^$"),
    "BEGIN_SLASH_NUMERAL": re.compile("^/|^#"),
}

#Funcion para leer un archivo y filtar las lineas que no se necesitan
def readDomains(file_name):
    lista = ""
    try:
        file_open =  open(file_name, "r")
        for linea in file_open.readlines():
            if linea == '\n':
                pass
            elif DELETE_PATTERN["BEGIN_SLASH_NUMERAL"].match(linea):
                pass
            else:
                lista += linea
    except:
        return lista
    else:
        return lista


#Funcion para que se inicie la lectura de todos los archivos con listas negras
def readFiles():
    listas = ""
    for i in range(NUMBER_OF_FILES):
        listas += readDomains(f"{i+1}.txt")
    return listas.split('\n')
    
#Funcion principal (el programa)
def main():
    listfile = readFiles()
    blacklist = ""

    for line in listfile:
        #Filtrado de los dominios para que esten bien escritos
        has_www = SEARCH_PATTERN["HAS_WWW"].match(line)
        has_http = SEARCH_PATTERN["HAS_HTTP"].match(line)
        has_ip = SEARCH_PATTERN["HAS_IP_AND_PORT"].match(line)
        if has_ip:
            blacklist = blacklist + f"{PRE_STRING}{has_ip[1]}{POST_STRING}\n"
        elif has_www:
            blacklist = blacklist + f"{PRE_STRING}{has_www[0]}{POST_STRING}\n"
        elif has_http:
            blacklist = blacklist + f"{PRE_STRING}{has_http[1]}{POST_STRING}\n"
        elif line == '':
            pass
        else:
            blacklist = blacklist + f"{PRE_STRING}{line}{POST_STRING}\n"
    
    with open(FILE_NAME, "w") as file:
        file.writelines(blacklist[:-1])
        
if __name__ == '__main__':
    main()
