import os
from flask import Flask, render_template, send_from_directory, request, redirect
import csv

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template("index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


template_list=os.listdir('./templates')

@app.route('/<content_page>')
def content_page(content_page):
    if content_page in template_list:
        return render_template(content_page)
    else:
        return render_template("index.html")


def save_message_data_txt(data):
    with open("./database.txt", mode="a") as database:
        email=data["email"]
        subject=data["subject"]
        message=data["message"]
        database.write(f"\n{email},{subject},{message}")
        return 'data saved!'


def save_message_data_csv(data):
    with open("./database.csv", mode="a", newline='') as database2:
        email=data["email"]
        subject=data["subject"]
        message=data["message"]
        csv_writer=csv.writer(database2, quoting=csv.QUOTE_NONE)
        csv_writer.writerow([email,subject,message])
        return 'data saved!'


@app.route('/send_message', methods=['POST', 'GET'])
def send_message():
    if request.method=='POST':
        try:
            data=request.form.to_dict()
            save_message_data_csv(data)
            return redirect("thanks.html")
        except:
            return 'Data weren\'t saved, fix it!'
    else:
        return 'Something went wrong, please try again.'
