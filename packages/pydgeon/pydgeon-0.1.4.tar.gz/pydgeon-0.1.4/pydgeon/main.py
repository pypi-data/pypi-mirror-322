# pydgeon/main.py

import os
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


_credentials = {}

def dovecot(senderMail, passKey):
    global _credentials
    _credentials['senderMail'] = senderMail
    _credentials['passKey'] = passKey
    return _credentials





def coo(subject, body, recieverMail):
    global _credentials
    print(f"Sending with {subject}, {body}, {recieverMail}")
    msg = EmailMessage()
    msg['From'] = _credentials['senderMail']
    msg['To'] = recieverMail
    msg['Subject'] = subject
    msg.set_content(body)

    # Connect to smtplib and send email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(_credentials['senderMail'], _credentials['passKey'])
            smtp.send_message(msg)
            print("Email sent succesfully!")
    except Exception as e:
        print("Failed to send email!", e)




def hoot(subject, body, attachmentPath, recieverMail):
    global _credentials
    print(f"Sending with {subject}, {body}, {attachmentPath}, {recieverMail}")

    # Setup the MIME
    msg = MIMEMultipart()
    msg["From"] = _credentials['senderMail']
    msg["To"] = ", ".join(recieverMail)
    msg["Subject"] = subject

    # Attach the body text
    msg.attach(MIMEText(body, "plain"))

    # Handle attachment
    if attachmentPath:
        try:
            # Extract filename
            fileName = os.path.basename(attachmentPath)

            # Open and attach the file
            with open(attachmentPath, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={fileName}",
            )
            msg.attach(part)

        except FileNotFoundError:
            print(f"Error: The file {attachmentPath} was not found.")
            return
        except Exception as e:
            print(f"An error occurred while processing the attachment: {e}")
            return
        except SyntaxError:
                print("Error! please use raw string: (" + r"C:\Example\Path\To\File.txt" + "), double backslashes: (\\), or forward slashes: (/)")
                return
        
        # Connect to smtplib and send email with attachment
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(_credentials['senderMail'], _credentials['passKey'])
                smtp.send_message(msg)
                print("Email sent succesfully!")
        except Exception as e:
            print("Failed to send email!", e)