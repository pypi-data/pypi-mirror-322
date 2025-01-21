# pydgeon/main.py

import os
import smtplib
import datetime as dt
import time
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

    # Ensure receiverMail is always a list
    if isinstance(receiverMail, str):
        receiverMail = [receiverMail]  # If it's a single string, convert to list
    elif not isinstance(receiverMail, list):
        print("Error: receiverMail must be a string or a list of strings.")
        return

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




def hoot(subject, body, attachmentPath, receiverMail):
    global _credentials
    print(f"Sending with {subject}, {body}, {attachmentPath}, {receiverMail}")

    # Ensure receiverMail is always a list
    if isinstance(receiverMail, str):
        receiverMail = [receiverMail]  # If it's a single string, convert to list
    elif not isinstance(receiverMail, list):
        print("Error: receiverMail must be a string or a list of strings.")
        return

    # Setup the MIME
    msg = MIMEMultipart()
    msg["From"] = _credentials['senderMail']
    msg["To"] = ", ".join(receiverMail)
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




def cooAt(subject, body, hour, minute, receiverMail, checkDelay=10, exitAfter=True):
    """
    Sends a text-only email at a specified time.
    
    Parameters:
        subject (str): The subject of the email
        body (str): The body of the email
        hour (int): At which hour to send the email
        minute (int): At which minute to send the email
        receiverMail (str): Which email address to send to
    
    Returns:
        Nothing
    """

    emailSent = False
    global _credentials
    print(f"Sending with {subject}, {body}, {receiverMail}")

    # Ensure receiverMail is always a list
    if isinstance(receiverMail, str):
        receiverMail = [receiverMail]  # If it's a single string, convert to list
    elif not isinstance(receiverMail, list):
        print("Error: receiverMail must be a string or a list of strings.")
        return

    msg = EmailMessage()
    msg['From'] = _credentials['senderMail']
    msg['To'] = receiverMail
    msg['Subject'] = subject
    msg.set_content(body)



    while True:
        currentTime = dt.datetime.now()
        if currentTime.hour == hour and currentTime.minute == minute and not emailSent:
            print("Sending Email!")
            
            # Connect to smtplib and send email
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.starttls()
                    smtp.login(_credentials['senderMail'], _credentials['passKey'])
                    smtp.send_message(msg)
                    print("Email sent succesfully!")
                    if exitAfter == True:
                        print("Exiting loop!")
                        break
            except Exception as e:
                print("Failed to send email!", e)


            emailSent = True  # Correctly update the flag

        # Reset the flag after the minute changes
        if currentTime.hour != hour or currentTime.minute != minute:
            emailSent = False

        # Wait a short while before checking again
        time.sleep(checkDelay)
        print("Checking time...")




def hootAt(subject, body, attachmentPath, hour, minute, receiverMail, checkDelay=10, exitAfter=True):
    emailSent = False
    global _credentials
    print(f"Sending with {subject}, {body}, {attachmentPath}, {receiverMail}")

    # Ensure receiverMail is always a list
    if isinstance(receiverMail, str):
        receiverMail = [receiverMail]  # If it's a single string, convert to list
    elif not isinstance(receiverMail, list):
        print("Error: receiverMail must be a string or a list of strings.")
        return

    # Setup the MIME
    msg = MIMEMultipart()
    msg["From"] = _credentials['senderMail']
    msg["To"] = ", ".join(receiverMail)
    msg["Subject"] = subject

    # Attach the body text
    msg.attach(MIMEText(body, "plain"))

    while True:
        currentTime = dt.datetime.now()
        if currentTime.hour == hour and currentTime.minute == minute and not emailSent:
            print("Sending Email!")

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
                        if exitAfter == True:
                            print("Exiting loop!")
                            break
                except Exception as e:
                    print("Failed to send email!", e)

            # Reset the flag after the minute changes
            if currentTime.hour != hour or currentTime.minute != minute:
                emailSent = False

        # Wait a short while before checking again
        time.sleep(checkDelay)
        print("Checking time...")