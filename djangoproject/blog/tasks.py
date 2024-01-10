from time import sleep
from django.core.mail import send_mail
from celery import shared_task


@shared_task()
def send_feedback_email_task(email, message):
    send_mail(
        'Обратная связь с блога',
        f'Отправитель: {email}\n\n'
        f'Сообщение: {message}',
        '',
        ['oleg.fisenko2013@yandex.ru'],
        fail_silently=False
    )
