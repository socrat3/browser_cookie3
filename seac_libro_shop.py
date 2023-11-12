## scarica seac v. 0.4 del 05-11-2023 dallo shop, devi controllare l'anteprima e con f12 di chrome rilevare la url che scarica la pagina, poi vai in network e cerca la pagina pdf che hai visualizzato con lo scorrimento delle pagine. Devi andare in shop seac ed entrare nella visualizzazione dei libri comprati es Agricoltura copiare il codicelibro md5 e il token
import requests
import shutil
import hashlib
import os
import subprocess
import argparse
import re
import shlex
import pdfrw
import time
import browser_cookie3
# Per gestione PDF
from PyPDF2 import PdfMerger, PdfReader
# per invio email sender
import smtplib, os
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
requests.packages.urllib3.disable_warnings()
# specificare anno e nr iniziale rivista e finale
# 1) AF PER INFORMATIVA FISCALE ULTIMA SCARICATA 67
# 2) AP PER INFORMATIVA PERSONALE SEAC ULTIMA SCARICATA 122
# 3) SETTIMANA PROFESSIONALE SPCF209_1
# 4) il NOTIZIARIO - NOT2005FULL 
# 5) mondo terzo settore MTS21008
# 6) GESTIONE BONUS ITSEB21024
# 7) MONDO PAGHE MP1912FULL
# 8) Mondo terzo settore MTS21008
# 9) Le SCHEDE OPERATIVE FISCALI SOF0349_00
# 10) LE SCHEDE OPERATIVE GESTIONE DEL PERSONALE SOL0001_00
# 11) ISA SEAC ITSIS20003
# 12) SEAC PRIVACY ITSPR19001
# 13) SEAC ANTIRICICLAGGIO ITSAR19001
# 14) SEAC GESTIONE FATTURAZIONE ELETTRONICA ITS18001
# 15) SEAC CORRISPETTIVI TELEMATICI ITSCT21046
# 16) SEAC Informative Comunitarie del Personale APCOM21189
# 17) SEAC Info Aziende Fiscale AF21004B LA B è MAIUSCOLA
# 18) SEAC INFO AZIENDE LAVORO AP21004B - LA B FINALE è MAIUSCOLA
# 19) SEAC CCNL 100 APCCNL21040
# 20) manuale iva 2022  https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=d9ea48eb269de2570f96847fd98e49f8db376e10.pdf&format=pdf&subfolder=9238&page= http://all-in.seac.it/assets/library/NOVIT%C3%80-FISCALI-2020/files/assets/common/downloads/page0038.pdf?uni=2c5100b5c274b86fdf1ecdb2ee0380ef
# 21) SEAC AUTOVETTURE 2022 https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=bc23dcde2706ac1d7e4b34286ebb41cbc9f20e9f.pdf&format=pdf&subfolder=9963&page=
# 22 LOCAZIONI IMMOBILIARI 2023 https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=4ab5eb38e0984ee31a0a9e017a7ae117a378a667.pdf&format=pdf&subfolder=10643&page=
# 23 SPESE DI RAPPRESENTANZA https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=05a8a2f4040fdb2b4650b338a49f74dc0b5222fd.pdf&format=pdf&subfolder=8554&page= 
# AGEVOLAZIONI https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=d83601ab73917415e6dcf61e645c435600a44d66.pdf&format=pdf&subfolder=10153&page=
# CONFERIMENTO D'AZIENDA https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=94cf1cb9f044d29276215c4a8bd94764a5c34aaf.pdf&format=pdf&subfolder=9880&page=
# SRL https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=5473bd41375c96e37a4f21ca89a796894633f65c.pdf&format=pdf&subfolder=9413&page=
# AGRICOLTURA FISCO https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=d082f44380094149f2141a2577b3e6219c0fc7fd.pdf&format=pdf&subfolder=6878&page=3
# superbonus 2023 https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=586a01c7cbd175388aa78a27c40c00d4b7793b7e.pdf&format=pdf&subfolder=9891&page=
# ASSOCIAZIONI SPORTIVE DILETTANTISTICHE 2023 https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=dfecf6be8698447983806c48c4687fdb3355d13e.pdf&format=pdf&subfolder=9882&page=
# antiriciclaggio 2023 https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=ebb92e3a5a95b725766c44f996ee6f7894b8b050.pdf&format=pdf&subfolder=9879&page=3
# percorso chrome del file sql doe prendere i dati della sessione
chromecookies = os.path.join(os.path.expandvars("%userprofile%"),"AppData\\Local\\Google\\Chrome\\User Data\\Guest Profile\\Cookies")
# Impostare i dati del libro da scaricare unire e inviare via email
testo = "_TESTO_"
informativafiscale = "Antiriciclaggio2023"
libro = informativafiscale
anno = 20
nrpaginainizio = 1 # nr pagina iniziale da scaricae
nrpaginetotalilibro = 280 ## nr 1359 pagine totali da scaricare
path = r'seac_libro_' + str(libro) + '_' + str(anno)
urlseaclibro = "https://shop.seac.it/modules/seacpreview/flowpaper/services/view.php?doc=ebb92e3a5a95b725766c44f996ee6f7894b8b050.pdf&format=pdf&subfolder=9879&page="
# Dati email gmail.com
user = "cafsicilia" #Your Gmail
password = "exsbtexiivmdzspc" #Your password
recipient = "salvatore.crapanzano@gmail.com" #Recipient
directory = 'D:\seac_libro_' + '/' + path + '/'

# creazione oggetto pdf
pdf_merger = PdfMerger()
# IMPOSTA IL NR. DELLA RIVISTA DA SCARICARE
nr = nrpaginainizio
nrfinale = (nrpaginetotalilibro + 1) 

# DATI CONNESSIONE SERVER GMAIL


def download_file(url):
    headers = {
    'authority': 'shop.seac.it',
    'sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'Accept-Encoding': 'gzip, deflate',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
    'sec-ch-ua': '.Not/A)Brand";v="99; Google Chrome;v=103, Chromium;v=103',
    'Origin': 'https://shop.seac.it',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

    chromecookies = os.path.join(os.path.expandvars("%userprofile%"),"AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies")
    cj = browser_cookie3.chrome(cookie_file=chromecookies)
    if not os.path.exists(path):
        os.makedirs(path)
    with requests.get(url, url, headers=headers, verify=False, cookies=cj, stream=True) as r:
        with open(path + '/' + nomefileinformativafiscaleEXT, 'wb') as f:
            f.write(r.content)
            #shutil.copyfileobj(r.raw, f)
            # shutil.copytree (dirname1, dirname2)

    return nomefileinformativafiscaleEXT


#seacmail = "http://all-in.seac.it/assets/library/'+ libro + '/files/assets/common/downloads/page' + nr + '.pdf?uni=2c5100b5c274b86fdf1ecdb2ee0380ef"


intervallo = range(nr,nrfinale)
merger = PdfMerger()
for nr in intervallo:
    #nr = str(nr).rjust(4, '0')
    seacmail = urlseaclibro + str(nr)+'&token=6a89e14213ffd5190b2a44f1e4861adb'
    nomefileinformativafiscale = informativafiscale + '_' + str(anno) + '_' + str(nr) + 'FULL'
    print(seacmail)
    nomefileinformativafiscaleEXT = nomefileinformativafiscale + '.pdf'
    nomefileinformativafiscaleEXT2 = nomefileinformativafiscale + '.pdf'
    print(seacmail)
    #print(hashlib.md5(nomefileinformativafiscale.encode('utf-8')).hexdigest())
    #md5 = hashlib.md5(nomefileinformativafiscale.encode('utf-8')).hexdigest()
    percorsofile = path + '/' + nomefileinformativafiscaleEXT
    percorsofile2 = path + '/' + nomefileinformativafiscaleEXT + '_e.pdf'
    nomefilepdfunicofull = path + '/' + str(libro) + str(anno) + '.pdf'
    print(nomefilepdfunicofull)
    url = seacmail
    solonomefilepdfunicofull = str(libro) + str(anno) + '.pdf'
    
    print(url)
    print("il percorso è: ", percorsofile)

    download_file(url)
    subprocess.call(['gswin64c.exe', '-sDEVICE=pdfwrite', '-dBATCH', '-dNOPAUSE', '-sOutputFile={}' .format(percorsofile2), percorsofile], shell=True)
    print("Verra' tolta la seguente frase:", testo)
    subprocess.call(['pdfremover.py', '-f{}' .format(percorsofile2), '-s{}' .format(testo)], shell=True)
    subprocess.call(['gswin64c.exe', '-sDEVICE=pdfwrite', '-dBATCH', '-dNOPAUSE', '-sOutputFile={}' .format(percorsofile), percorsofile2], shell=True)
    # subprocess.call(['dropbox_uplload.py', '--tgt', '/', '--src', 'percorsofile2'])
    merger.append(percorsofile)
    
    os.remove(percorsofile2)
merger.write(str(nomefilepdfunicofull))
merger.close()

## copio in maniera ricorsiva i file trattati
root_src_dir = path    #Path/Location of the source directory
root_dst_dir = 'D:\seac_libro_' + '/' + path #Path to the destination folder

for src_dir, dirs, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        print("sono qui", src_file)
        print("sono qui noe", nomefilepdfunicofull)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        if  file_ == solonomefilepdfunicofull: # copio solo file pdf unico
            print("sono qui", src_file)
            print("confronto qui", solonomefilepdfunicofull)
            shutil.copy(src_file, dst_dir)#
        
if os.path.exists(root_src_dir):
    shutil.rmtree(root_src_dir)
# CICLO CHE INVIA EMAIL

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(user, password)

eBooks = []
for file in [doc for doc in os.
    listdir(directory)]:
    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Subject'] = "Invio libro " + libro + " " + str(anno)
    body = "Ho terminato di scaricare il libro"
    msg.attach(MIMEText(body, "plain"))
    try:
        file = directory+file
        attachment = open(file, "rb")
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename= "+file)
        msg.attach(part)
        text = msg.as_string()
        server.sendmail(user, recipient, text)
        attachment.close()
        file = file.replace(directory, "")
        print(file + " inviato! Prego padrone!")
    except:
        file = file.replace(directory, "")
        print(file + " Invio email fallito!")
server.quit()