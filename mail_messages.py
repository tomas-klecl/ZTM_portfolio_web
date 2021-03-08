import smtplib, ssl
from email.message import EmailMessage
import os

msg = EmailMessage()

msg['From'] = 'your_developer_email_account'
msg['To'] = 'your_personnal_email_account'
msg['Subject'] = 'Messages from your website'
password = 'your_super_secret_developer_email_account_password'
SMTP_server = 'smtp.gmail.com'
port = 465

# preventing file path issues when set as a daily run task
script_directory = os.path.dirname(os.path.abspath(__file__))
message_file_directory = os.path.join(script_directory, 'new_messages.txt')


def check_for_messages():
    with open(message_file_directory, mode="r", encoding="utf-8") as message_file:
        messages = message_file.read()
        if len(messages) > 0:
            try:
                send_messages(messages)
                print('email has been sent')
            # preventing the deletion of new_messages.txt content when the email sending fails
            except Exception as e:
                return print(f'{e}, message sending has failed')

            with open(message_file_directory, mode="w") as f:
                return print('new_messages content has been deleted')
        else:
            return print('no messages have been received, going to sleep...')


def send_messages(messages):
    # create a secure SSL context
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_server, port, context=context) as server:
        server.login(msg['From'], password)
        msg.set_content(messages)
        server.send_message(msg)


if __name__ == '__main__':
    check_for_messages()
