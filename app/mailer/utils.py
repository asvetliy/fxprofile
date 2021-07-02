from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class Mailer(object):
    @classmethod
    def send(cls, action: str, user, subject: str = '', params: dict = None):
        mail_message_html = render_to_string(f'mailer/{action}.html', params)
        mail_message_txt = render_to_string(f'mailer/{action}.txt', params)
        send_mail(
            subject=subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            message=mail_message_txt,
            html_message=mail_message_html,
            fail_silently=False
        )

    @classmethod
    def send_admin(cls, from_, to_):
        pass

    @classmethod
    def send_managers(cls, action: str, subject: str = '', params: dict = None):
        mail_message_html = render_to_string(f'mailer/managers/{action}.html', params)
        mail_message_txt = render_to_string(f'mailer/managers/{action}.txt', params)
        send_mail(
            subject=subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.MANAGERS,
            message=mail_message_txt,
            html_message=mail_message_html,
            fail_silently=False
        )

