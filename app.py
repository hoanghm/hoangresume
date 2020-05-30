from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import required, Email
from flask_mail import Mail, Message
from flask_login import current_user
import os


# config
class Config:
    SECRET_KEY = "abcde"
    # SECRET_KEY = os.environ .get("SECRET_KEY")
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    RESUME_LINK = os.environ.get("RESUME_LINK")
    MAIL_DEFAULT_SENDER = 'hoanghm4@gmail.com'


'''
Initialize the app
'''
app = Flask(__name__)
app.config.from_object(Config)

# Intialize mail server
mail = Mail()
mail.init_app(app)



class ContactForm(Form):
    name = StringField( validators=[required()])
    email = StringField(validators=[required(), Email()])
    message = TextAreaField(validators=[required()])
    submit = SubmitField(label="Send Inquiry")

def send_email(to, subject, template, **kwargs):
    msg = Message("[MyResume]" + subject, recipients=[to])
    msg.body = template
    mail.send(msg)

class InquiryManager():
    def __init__(self):
        self.submitted = False
        self.guest_name = None
    def getSubmitted(self):
        return self.submitted
    def getGuestName(self):
        return self.guest_name
    def setSubmitted(self, val):
        self.submitted = val
    def setGuestName(self, name):
        self.guest_name = name

@app.before_request
def before_request():
    print("headers: ",request.headers, "/n-------------")
    print("type: ", type(request.headers))


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        send_email("hoanghm4@gmail.com", name, message + " " + email)
        return redirect(url_for("form_submitted"))
    return render_template('index.html', form=form, resume_link=app.config["RESUME_LINK"], submitted=False)

@app.route('/submitted', methods=['GET', 'POST'])
def form_submitted():
    form = ContactForm()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        send_email("hoanghm4@gmail.com", name, message + " " + email)
        return redirect(url_for("form_submitted"))
    return render_template('index.html', form=form, resume_link=app.config["RESUME_LINK"], submitted=True)

@app.route('/<anything>')
def error_404(anything):
    return "<h1> Hey! Where do you think you're going buddy? </h1> "


if __name__ == '__main__':
    app.run()
