#!/usr/bin/python3

# Import modules
from qrGenerator import *
from walletPass import *
import smtplib, ssl
## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#--------------------------------------------------------EMAIL-----------------------------------------------------------------------#


#Funcion para adjuntar imagenes al email
def attach_file_to_email(email_message, filename, extra_headers=None):
    # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
    with open(filename, "rb") as f:
        #file_attachment = MIMEApplication(f.read())
        file_attachment=MIMEImage(f.read())
    # Add header/name to the attachments    
    file_attachment.add_header("Content-Disposition", f"attachment; filename= {filename}")

    # Set up the input extra_headers for img
      ## Default is None: since for regular file attachments, it's not needed
      ## When given a value: the following code will run
         ### Used to set the cid for image
    if extra_headers is not None:
        for name, value in extra_headers.items():
            file_attachment.add_header(name, value)
    # Attach the file to the message
    email_message.attach(file_attachment)

#Contraseña generada en el link https://myaccount.google.com/u/0/apppasswords  
def email_sender(email_to,destino,saveLink):

    #Generamos QR con el saveLink del pase
    qrGenerator(saveLink)

    #--------------------------------------------------------Preparar y mandar email-----------------------------------------------------------------------#
    email_from = 'pruebas.catedra.masmovil@gmail.com'
    password = 'hfnxbpginhyjdkob'
    #email_to = 'pruebas.catedra.masmovil@gmail.com'

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'¡Bienvenido a PepePhone!'

    # write the HTML part
    html = """
        <html>
        <body>
            <p>Hola <b>"""+destino+"""</b>,</p>
            <p>Gracias por confiar en PepePhone. 
                <br>
                <br>
                Clickando el siguiente
                <a href="""+saveLink+""">enlace</a>
                o botón podrás añadir tu contrato a tu wallet.
                <br>
                Si lo prefieres escanea el código QR para añadir tu contrato a Google Wallet.
            </p>
            <p>
                ¡Hasta pronto!,
                <br>
                El equipo de PepePhone
                <br> 
            </p>
            <p margin-top="100">
                <a href="""+saveLink+"""><img src='cid:walletButtonid' alt="wallet-button.png" width="300"></a>
            </p>
            <p margin-top="100" margin-bottom="100"> 
                <img src='cid:qrcodeid' width="300" height="300" alt="contratoQR.png">
            </p> 
        </body>
        </html>
        """

    #Convertimos el codigo html a  objetos MIMEText y lo añadimos al mensaje MIMEMultipart 
    parteHtml = MIMEText(html, "html")
    email_message.attach(parteHtml)

    attach_file_to_email(email_message, '/home/samuel/Desktop/googleWallet_prototipo/resources/contratoQR.png', {'Content-ID': '<qrcodeid>'})
    attach_file_to_email(email_message, '/home/samuel/Desktop/googleWallet_prototipo/resources/wallet-button.png', {'Content-ID': '<walletButtonid>'})
    #attach_file_to_email(email_message, f'contrato.pdf')

    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_from, password)
        server.sendmail(email_from, email_to, email_string) 
        #server.send_message(email_message)


