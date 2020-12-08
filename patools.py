import email, smtplib, ssl, os, requests, subprocess, pickle, argparse, socket
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import *
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image

def cesar(frase,clave):
    frase = frase.upper()
    # Aqui el usuario introduce el numero correspondiente a la posicion de la letra
    # del abecedario
    abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    cifrado = ""
    for letra in frase:
    # Si la letra está en el abecedario se reemplaza
        if letra in abc:
            pos_letra = abc.index(letra)
        # Suma para moverse hacia la derecha el abecedario
            nueva_pos = (pos_letra + clave) % len(abc)
            cifrado+= abc[nueva_pos]
        else:
        # Si es un simbolo que no esta en el diccionario se deja igual
            cifrado+= letra
    print("Mensaje cifrado:", cifrado)

def send_mail(remitente_email,password,destinatario_email,asunto,cuerpo,filename):
    # Headers del correo
    message = MIMEMultipart()
    message["From"] = remitente_email
    message["To"] = destinatario_email
    message["Subject"] = asunto
    message.attach(MIMEText(cuerpo, "plain"))
    #Agrega el archivo a adjuntar 
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    # Codifica el archivo a base64   
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    message.attach(part)
    texto = message.as_string()
    # Inicia sesión en el server y despúes envia el correo
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(remitente_email, password)
        server.sendmail(remitente_email, destinatario_email, texto)

def get_images(url, ruta):
    r=requests.get('http://www.'+url)
    soup= BeautifulSoup(r.text, 'html.parser')
    urls=list()
    images=soup.select('img[src]')
    for img in images:
        urls.append(img['src'])
    os.mkdir(ruta)
    i=1
    for index, img_link in enumerate(urls):
        if i<=len(urls):
            img_data=requests.get(img_link).content
            with open(ruta+'\\'+str(index+1)+'.jpg', 'wb+') as f:
                f.write(img_data)
            i+=1
        else:
            f.close()
            break

def decode_gps_info(exif):
    gpsinfo = {}
    if 'GPSInfo' in exif:
        #Parse geo references.
        Nsec = exif['GPSInfo'][2][2] 
        Nmin = exif['GPSInfo'][2][1]
        Ndeg = exif['GPSInfo'][2][0]
        Wsec = exif['GPSInfo'][4][2]
        Wmin = exif['GPSInfo'][4][1]
        Wdeg = exif['GPSInfo'][4][0]
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][1] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        exif['GPSInfo'] = {"Lat" : Lat, "Lng" : Lng}
        input()
 
def get_exif_metadata(image_path):
    ret = {}
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        exifinfo = image._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    decode_gps_info(ret)
    return ret
    
def printMeta(ruta):
    os.chdir(ruta)
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            print(os.path.join(root, name))
            print ("[+] Metadata for file: %s " %(name))
            input()
            try:
                exifData = {}
                exif = get_exif_metadata(name)
                for metadata in exif:
                    print ("Metadata: %s - Value: %s " %(metadata, exif[metadata]))
                print ("\n")
            except:
                import sys, traceback
                traceback.print_exc(file=sys.stdout)

def scan_ports(target,begin,end):
    #Crea el socket
    sock = socket.socket()
    for port in range(int(begin),int(end)+1):
    #Se intenta conectar al puerto y en caso de error imprime Puerto Cerrado
        try:
            sock.connect((target,port))
            print("Puerto "+str(port)+" abierto")
            sock.close()
        except:
            print("Puerto "+str(port)+" cerrado.")

def ValidatePath(thePath):
    # Validate que el path existe
    if not os.path.exists(thePath):
        raise argparse.ArgumentTypeError('Path does not exist')
    # Validate que el path se puede leer
    if os.access(thePath, os.R_OK):
        return thePath
    else:
        raise argparse.ArgumentTypeError('Path is not readable')

def get_hashlist(baselineFile,targetPath,tmpFile):
    try:
        ''' Ejecución de Powershell '''
        print()
        command = "powershell -ExecutionPolicy ByPass -File HashAcquire.ps1 -TargetFolder "+\
                  targetPath + " -ResultFile " + tmpFile 
        print(command)
        powerShellResult = subprocess.run(command, stdout=subprocess.PIPE)
        if powerShellResult.stderr == None:       
            ''' Creacion del diccionario '''
            baseDict = {}           
            with open(tmpFile, 'r') as inFile:
                for eachLine in inFile:
                    lineList = eachLine.split()
                    if len(lineList) == 2:
                        hashValue = lineList[0]
                        fileName  = lineList[1]
                        baseDict[hashValue] = fileName
                    else:
                        continue        
            with open(baselineFile, 'wb') as outFile:
                pickle.dump(baseDict, outFile)
                print("Baseline: ", baselineFile, " Created with:",
                      "{:,}".format(len(baseDict)), "Records")
                print("Script Terminated Successfully")
        else:
            print("PowerShell Error:", p.stderr)            
    except Exception as err:
        print ("Cannot Create Output File: "+str(err))
        quit()
    


