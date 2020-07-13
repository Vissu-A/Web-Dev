# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.core.mail import send_mail

from time import sleep

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


@shared_task
def mailsend(uname, passcode, emid):

    message = Mail(
    from_email='django.mail@gmail.com',
    to_emails=emid,
    subject='Bookatore Account Creation',
    html_content='<strong>and easy to do anywhere, even with Python</strong>'
    )

    # data = {
    #     "from":{"email":"django.mail@gmail.com", "name": "Bookstore"},
    #     "subject": "Bookatore Account Creation",
    #     "personalizations":[{
    #         "to":[{"email": emid}],
    #     }]
    # }

    # data = {
    #         "from":{"email":"django.mail@gmail.com", "name": "Bookstore"},
    #         "subject": "Bookatore Account Creation",
    #         "template_id":"eeccc9d7-37b7-428c-9b21-20b0692e66ac",
    #         "personalizations":[{
    #             "to":[{"email": emid}],
    #             "substitutions":{
    #                 "%taskid%":str(taskid),
    #                 "%official_name%":str(official_name)
    #             }
    #         }]
    #     }

    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        return response.status_code

    except Exception as e:
        print('Exception is: ', e)
        return 400

    # try:
    #     sg = SendGridAPIClient('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')
    #     response = sg.client.mail.send.post(request_body=data)
    #     return ('status code is: ', response.status_code)
    # except Exception as e:
    #     print('Something went wrong')
    #     print(e)
    #     return 400

    # response = sg.client.mail.send.post(request_body=message.get())
    # return [response.status_code, response.body, response.headers]