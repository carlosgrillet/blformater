import logging
import re
import os

NUMBER_OF_FILES = 5
FILE_NAME = "blacklist.rsc"
PRE_STRING = "/ip firewall address-list add list=blacklist address="
POST_STRING = ";"

SEARCH_PATTERN = { 
    "HAS_HTTP": re.compile("(?:^http:\/\/)([a-z.]*)"),
    "HAS_WWW": re.compile("((?:w{3}\.)([a-z.]*))"),
    "HAS_IP_AND_PORT": re.compile("((?:w{3}\.)?(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}))"),
}

DELETE_PATTERN = { 
    "BLANK_LINE": re.compile("^$"),
    "BEGIN_SLASH_NUMERAL": re.compile("^/|^#"),
}

def readDomains(file_name):
    lista = ""
    with open(file_name , "r") as file_open:
        for linea in file_open.readlines():
            if linea == '\n':
                pass
            elif DELETE_PATTERN["BEGIN_SLASH_NUMERAL"].match(linea):
                pass
            else:
                lista += linea
    return lista

def readFiles():
    listas = ""
    for i in range(NUMBER_OF_FILES):
        listas += readDomains(f"{i+1}.txt")
    return listas.split('\n')
    
def main():
    listfile = readFiles()
    blacklist = ""

    for line in listfile:
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
