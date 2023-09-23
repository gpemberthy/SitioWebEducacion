import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def envio_correo(correo1, asunto1):
    
    # Configuración de la cuenta de Gmail
    sender_email = "german.pemberty@gmail.com"
    sender_password = "ottmedkbarfpgcfw"

    # Destinatario
    #recipient_email = "german.pemberthy@outlook.com"
    recipient_email = correo1

    # Crear el mensaje
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Prueba de envio"

    # Cuerpo del correo
    body = "Señor residente adjunto se encuentra el comprobante del ultimo pago realizado"
    message.attach(MIMEText(body, "plain"))

    # Adjuntar el documento
    file_path = "C:/Users/germa/Desktop/SitioWebEducacion/example2.pdf"  # Reemplaza con la ruta de tu documento
    filename = "example2.pdf"  # Nombre que tendrá el archivo adjunto en el correo
    attachment = open(file_path, "rb")

    part = MIMEBase("application", "octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")

    message.attach(part)

    # Iniciar la conexión con el servidor SMTP de Gmail
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Enviar el correo
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Correo enviado con éxito")

    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")

    finally:
        # Cerrar la conexión con el servidor
        server.quit()

z1="german.pemberthy@outlook.com"
t1="lizeth.mantilla7@gmail.com"
envio_correo(z1, t1)
