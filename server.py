import os
from flask import Flask, render_template, send_from_directory, request, redirect
import csv
import re
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<content_page>')
def content_page(content_page):
    template_list = os.listdir('./templates')
    if content_page in template_list:
        return render_template(content_page)
    else:
        return render_template("index.html")


def save_message_data(data):
    with open("./database.csv", mode="a", newline='', encoding='utf-8') as database:
        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        email = data["email"]
        subject = data["subject"]
        message = re.sub(r"\r?\n", " ", data["message"])  # remove Unix and Windows newlines
        csv_writer = csv.writer(database, quoting=csv.QUOTE_MINIMAL, delimiter='|')
        csv_writer.writerow([date_time, email, subject, message])

        with open("./new_messages.txt", mode="a", encoding='utf-8') as new_mes:
            new_mes.write(date_time + '\n' + email + '\n' + subject + '\n' + message + '\n\n')
    return 'data have been saved!'


@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            save_message_data(data)
            return redirect("thanks.html")
        except Exception as e:
            return (f'Exception \"{e}\" received. Please let me know on tomas.klecl@seznam.cz ' +
                    'how you filled out this form, so that I can replicate the issue and fix it.')
    else:
        return ('Something went wrong, POST request method has failed. Please let me know on ' +
                'tomas.klecl@seznam.cz what steps you took, so that I can replicate the issue and fix it.')
