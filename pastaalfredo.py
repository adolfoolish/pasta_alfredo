import argparse, logging
from patools import *

def main():
    descripcion = """ \n--------------------Bienvenido--------------------

        1) Cifrado Cesar de cualquier mensaje.
        ----> Ejemplo:  -cifrar "hola mundo" -clave 6

        2) Escanear los puertos de una IP para conocer su estado.
        ----> Ejemplo: -host 127.0.0.1 -comienzo 80 -final 81
            
        3) Enviar email con archivo adjunto.
        ----> Ejemplo: -r micorreo@gmail.com -passw mipassw -d destinatario@gmail.com -a asunto -cuerpo mensaje -adj archivo.pdf
       
        4) Descarga todas las imagenes de un sitio web y extrae su metadata;
        ----> Ejemplo: -link paginaweb.com -path C:/windows/system32

        5) Obtiene el valor hash de todos los archivos del directorio indicado y lo guarda en un
            archivo txt y pickle.
        ----> Ejemplo: -b ejemplo.pickle -p C:/windows/system32 -t ejemplo.txt

                                                                                """
    parser = argparse.ArgumentParser(descripcion)
    # Parser de cifrado cesar
    cifrado = parser.add_argument_group("------------------Cifrado Cesar-----------------------\n")
    cifrado.add_argument('-cifrar', '--mensaje',
                        help='El mensaje a encriptar, escribelo entre comillas dobles (" ")')
    cifrado.add_argument('-clave', '--key', help="La clave para cifrar el mensaje", type=int, default=5)
    # Parser del escaneo de puertos
    escaneo = parser.add_argument_group("-----------------Escaneo de Puertos-------------------\n")
    escaneo.add_argument('-host', '--scan', help="El host que se va a escanear")
    escaneo.add_argument('-comienzo', '--begin', type=int, default=80)
    escaneo.add_argument('-final', '--end', type=int, default=80)
    # Parser del envio de correos con adjuntos
    correo = parser.add_argument_group("---------------Enviar correo electronico---------------\n")
    correo.add_argument('-r', '--sender', help="Tu correo electronico de gmail")
    correo.add_argument('-passw', '--contra', help="El password para acceder a tu cuenta")
    correo.add_argument('-d', '--dest', help="La direccion destino del correo")
    correo.add_argument('-a', '--asunto', help="El asunto del correo")
    correo.add_argument('-cuerpo', '--body', help="El cuerpo del correo")
    correo.add_argument('-adj', '--adjunto', 
    help="El archivo que vas a adjuntar al correo, debe estar en el mismo path que el script")
    #Parser de extraccion de metadata
    metadata = parser.add_argument_group("--------Extraccion de metadata de todas las imagenes de una pagina web--------\n")
    metadata.add_argument('-link', '--url', help="El url de la web de donde deseas extraer la metadata")
    metadata.add_argument('-path', '--ruta',
    help="La ruta y nombre donde se creara la carpeta con las imagenes")
    # Parser de obtencion de hash
    hashes = parser.add_argument_group("-----Obtencion del hash de los archivos de un directorio-----\n")
    hashes.add_argument('-b', '--baseline', help="El nombre del archivo pickle")
    hashes.add_argument('-p', '--Path', help="El directorio donde se obtendran los hash (path absoluto)", 
    type=ValidatePath)
    hashes.add_argument('-t', '--tmp', help="El nombre del archivo txt")            
    args = parser.parse_args()
    if args.mensaje:
        logging.info('Cifrado cesar ejecutado')
        cesar(args.mensaje, args.key)
    elif args.scan:
        logging.info('Escaneo de puertos ejecutado')
        scan_ports(args.scan,args.begin,args.end)
    elif args.sender:
        logging.info('Envio de correo electronico ejecutado')
        send_mail(args.sender,args.contra,args.dest,args.asunto,args.body,args.adjunto)
        print('Correo enviado con exito')
    elif args.url:
        logging.info('Descarga y extraccion de metadata de imagenes ejecutado')
        get_images(args.url, args.ruta)
        printMeta(args.ruta)
    elif args.baseline:
        logging.info('Obtencion de hash')
        get_hashlist(args.baseline,args.Path,args.tmp)

if __name__ == "__main__":
    try:
        logging.basicConfig(
        format = '%(asctime)-5s %(name)-15s %(levelname)-8s %(message)s',
        level  = logging.INFO,
        filename = "logs_info.log",
        filemode = "a"                                 
    )
        logging.info('Ejecucion del script')
        main()
        logging.info('Script ejecutado')
        logging.shutdown()
    except:
        pass
        logging.error("Ocurrio un error de argumentos")



        
    



   
