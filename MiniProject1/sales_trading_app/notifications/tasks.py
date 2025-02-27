from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_notification_email(subject, message, recipient_list):
    send_mail(subject, message, 'zbagytzhan@gmail.com', recipient_list)