import imaplib
import email
from email.header import decode_header

from .models import EmailMessage


password = "***"
username = "***"

def mailru_importer():
        
    mail = imaplib.IMAP4_SSL("imap.mail.ru")


    mail.login(username, password)


    mail.select("inbox")


    status, messages = mail.search(None, "ALL")


    mail_ids = messages[0].split()

    for mail_id in mail_ids[0:1001]:
        
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        
        
        msg = email.message_from_bytes(msg_data[0][1])
        subject, encoding = decode_header(msg["Subject"])[0]

        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')
        
        
        sender = msg["From"]

        received_date = email.utils.parsedate_to_datetime(msg["Date"])
        
        file_data = 0

        if msg.is_multipart():
            for part in msg.walk():
                # Проверяем, является ли часть вложением
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()
                    if filename:
                        # Декодируем имя файла
                        decoded_filename = decode_header(filename)[0][0]
                        if isinstance(decoded_filename, bytes):
                            decoded_filename = decoded_filename.decode()

                        # Получаем данные файла
                        file_data = part.get_payload(decode=True)
                        EmailMessage.objects.create(
                            subject=subject, 
                            sender=sender, 
                            receiver='mail.ru', 
                            body=body,
                            attachments = file_data
                            )
                            
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                    

                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    
        else:
            body = msg.get_payload(decode=True).decode()

        if not file_data:
            EmailMessage.objects.create(
                subject=subject, 
                sender=sender, 
                receiver='mail.ru', 
                body=body,
                )


    mail.logout()

mailru_importer()