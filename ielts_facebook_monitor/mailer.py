''' send some emails '''

import configparser

from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
import transaction


credentials = configparser.ConfigParser()
credentials.read('credentials.ini')
smtp_settings = configparser.ConfigParser()
smtp_settings.read('gmail_smtp.ini')

settings = {
    'mail.host': smtp_settings['mail']['host'],
    'mail.port': smtp_settings['mail']['port'],
    'mail.ssl': smtp_settings['mail']['ssl'],
    'mail.username': credentials['mail']['username'],
    'mail.password': credentials['mail']['password']
}

mailer = Mailer.from_settings(settings)
message = Message(
    subject='this is a subject',
    sender='jerry.facebook.notify@gmail.com',
    recipients=['simon.bowly@gmail.com'],
    body='Hello, Simon')
mailer.send(message)
transaction.commit()
