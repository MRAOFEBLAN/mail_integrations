from django.core.management.base import BaseCommand
from email_service.gmail_importer import gmail_importer
from email_service.yandex_importer import yandex_importer
from email_service.mailru_importer import mailru_importer

class Command(BaseCommand):
    help = 'Импортировать электронные письма'

    def handle(self, *args, **kwargs):
        mailru_importer()
        gmail_importer()
        yandex_importer()
        