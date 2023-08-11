# blformater

[![GitHub Super-Linter](https://github.com/carlosgrillet/blformater/actions/workflows/linter.yml/badge.svg)](https://github.com/marketplace/actions/super-linter)

blformater es una herramienta para convertir listas de dominios, en listas de acceso para un router mikrotik, entre sus caracteristicas principales tenemos que nos permite:
 
- `Omitir lineas vacias`
- `Omitir lineas que sean comentarios`
- `Omitir lienas que sean solo rutas /home/web/index.html`
- `Filtrado de http://domain.com > domain.com`
- `filtrado de paginas www con ruta www.dominio.com/home/index.html > dominio.com`
- `filtrado de direcciones IP con puertos 200.201.202.203:8080 > 200.201.202.203`

> blformater toma como entrada de 1 a 5 archivos de texto de nombre `n.txt` ubicados en el mismo directorio donde esta el script
>
>     # Copyright (c) 2014-2023 Maltrail developers (https://github.com/stamparm/maltrail/)
>     # See the file 'LICENSE' for copying permission
>
>     # Aliases: gamarue
>
>     # Reference: http://www.microsoft.com/security/portal/threat/Encyclopedia/Entry.aspx?Name=Win32/Gamarue#tab=2
>
>     cityhotlove.com
>     clothesshopuppy.com
>     conpastcon.com
>     freefinder.me
>     grrrff24213402.com
>     grrrff2452.com
>     iurhjfnmflsdf.com
>     lanamakotrue.com
>     mgrsdfkprogerg.com
>     pastinwest.com
>     puppyclothesshop1.net
>     puppyclothesshop2.net
> 
> Como salida nos regresa un archivo llamado `blocklist.rsc`
>
>     /ip firewall address-list add list=blacklist address=cityhotlove.com;
>     /ip firewall address-list add list=blacklist address=clothesshopuppy.com;
>     /ip firewall address-list add list=blacklist address=conpastcon.com;
>     /ip firewall address-list add list=blacklist address=freefinder.me;
>     /ip firewall address-list add list=blacklist address=grrrff24213402.com;
>     /ip firewall address-list add list=blacklist address=grrrff2452.com;
>     /ip firewall address-list add list=blacklist address=iurhjfnmflsdf.com;
>     /ip firewall address-list add list=blacklist address=lanamakotrue.com;
>     /ip firewall address-list add list=blacklist address=mgrsdfkprogerg.com;
>     /ip firewall address-list add list=blacklist address=pastinwest.com;
>     /ip firewall address-list add list=blacklist address=puppyclothesshop1.net;
>     /ip firewall address-list add list=blacklist address=puppyclothesshop2.net;
>
> Adicionalmente nos genera un archivo llamado `lists.log` el cual nos permite ver si ha oacurrido un error
>
>     INFO 2023-02-06 14:26:18,004 - Iniciando el scritp
>     INFO 2023-02-06 14:26:18,004 - Abriendo archivo 1.txt
>     INFO 2023-02-06 14:26:18,004 - Leyendo archivo 1.txt
>     DEBUG 2023-02-06 14:26:18,004 - Omitida linea 1 Rason: / o # en ella
>     DEBUG 2023-02-06 14:26:18,005 - Omitida linea 6 Rason: Linea vacia
>     DEBUG 2023-02-06 14:26:18,005 - Omitida linea 11 Rason: Linea vacia
>     DEBUG 2023-02-06 14:26:18,005 - Omitida linea 12 Rason: Linea vacia
>     DEBUG 2023-02-06 14:26:18,005 - Omitida linea 13 Rason: Linea vacia
>     DEBUG 2023-02-06 14:26:18,005 - Omitida linea 14 Rason: / o # en ella
>     INFO 2023-02-06 14:26:18,005 - Archivo 1.txt leido con exito
>     INFO 2023-02-06 14:26:18,005 - Abriendo archivo 2.txt
>     INFO 2023-02-06 14:26:18,005 - Leyendo archivo 2.txt
>     INFO 2023-02-06 14:26:18,005 - Archivo 2.txt leido con exito
>     INFO 2023-02-06 14:26:18,005 - Abriendo archivo 3.txt
>     INFO 2023-02-06 14:26:18,005 - Leyendo archivo 3.txt
>     DEBUG 2023-02-06 14:26:18,005 - Omitida linea 6 Rason: / o # en ella
>     INFO 2023-02-06 14:26:18,006 - Archivo 3.txt leido con exito
>     INFO 2023-02-06 14:26:18,006 - Abriendo archivo 4.txt
>     ERROR 2023-02-06 14:26:18,006 - Omitiendo archivo 4.txt Rason: no encontrado
>     INFO 2023-02-06 14:26:18,006 - Abriendo archivo 5.txt
>     ERROR 2023-02-06 14:26:18,006 - Omitiendo archivo 5.txt Rason: no encontrado
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: cityhotlove.com
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: clothesshopuppy.com
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: conpastcon.com
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: freefinder.me
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: grrrff24213402.com
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: grrrff2452.com
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: iurhjfnmflsdf.com
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: lanamakotrue.com
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: mgrsdfkprogerg.com
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: pastinwest.com
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: puppyclothesshop1.net
>     DEBUG 2023-02-06 14:26:18,006 - Leyendo dominio: puppyclothesshop2.net
>     INFO 2023-02-06 14:26:18,008 - Escribiendo en archivo blacklist.rsc
>     INFO 2023-02-06 14:26:18,008 - Escritura finalizada

## Uso

Usando [python](https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe):

```bash
  python blformater.py
```

## Configuracion

El codigo tiene variables definidas que podemos ajustar a nuestra necesidad como;

- `Nombre del archivo de salida`
- `Nombre del archivo de log`
- `Numero maximo de archivos de entrada a leer`
- `Texto a colocar antes del dominio final`
- `Texto a colocar despues del dominio final`

```python
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
```

### Licencia
Desarrollado para Alejandro Cornieles
