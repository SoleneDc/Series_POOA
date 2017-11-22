from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from seriesDjangoProject import services
from django.core.mail import send_mail

class Command(BaseCommand):
    FROM_ADRESS = '1970annasmith@gmail.com'
    DAILY_MAIL_OBJECT = '[My series] Weekly alert'
    service = services.Services()

    def handle(self, *args, **options):
     """This function will send mails weekly with notifications to the users """

    users = User.objects.all()

    for user in users:
        if service.weekly_mail(user) is not None:
            send_mail(
                DAILY_MAIL_OBJECT,
                service.weekly_mail(user),
                FROM_ADRESS,
               [user.email],
                fail_silently=True,
            )
