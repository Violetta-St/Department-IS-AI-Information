from django.core.mail import EmailMessage

from celery_app import app


@app.task()
def send_login_and_password_to_email(user, login, password):
    message = f'{user.firstname}, логин и пароль для доступа к платформе:\n' \
              f'{login}\n{password}'
    email_message = EmailMessage(subject="Код подтверждения 'Мой финансовый помощник'", body=message, to=[user.email])
    email_message.send()
