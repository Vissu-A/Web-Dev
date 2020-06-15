# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.mail import send_mail

from time import sleep

@shared_task
def sendingmail(user, passcode, email):
    sleep(5)
    msg = 'Account credentials: '+str(user)+' : '+str(passcode)
    send_mail('Account creaated', msg, 'djangoclient9@gmail.com', [email])