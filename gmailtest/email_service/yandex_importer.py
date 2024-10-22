import imaplib
import email
from email.header import decode_header

from .models import EmailMessage



username = '***'
password = '***'

def yandex_importer():
    mail = imaplib.IMAP4_SSL("imap.yandex.ru")


    mail.login(username, password)

    mail.select("INBOX")


    status, messages = mail.search(None, "ALL")


    mail_ids = messages[0].split()

    for mail_id in mail_ids:
        
        status, msg_data = mail.fetch(mail_id, "(RFC822)")
        
        
        msg = email.message_from_bytes(msg_data[0][1])
        file_data = 0
        for part in msg.walk():
                    
            if part.get_content_disposition() == 'attachment':
                
                file_data = part.get_payload(decode=True)
        
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')
        
        
        sender = msg["From"]
        received_date = email.utils.parsedate_to_datetime(msg["Date"])
        
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        
        EmailMessage.objects.create(
            subject=subject,
            sender=sender,
            receiver='yandex.ru',
            body=body,
            attachments=file_data
        )


    mail.logout()
