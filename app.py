from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import required, Email
from flask_mail import Mail, Message
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


# @app.before_request
# def before_request():
#     if request.url.startswith('http://'):
#         url = request.url.replace('http://', 'https://', 1)
#         return redirect(url, code=301)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        send_email("hoanghm4@gmail.com", name, message + " " + email)
        flash("Inquiry received! Thank you for contacting me.")
        return redirect(url_for('index'))
    flash("testinggggggggggggg")
    return render_template('index.html', form=form)

@app.route('/<anything>')
def error_404(anything):
    return "<h1> Hey! Where do you think you're going buddy? </h1> "


if __name__ == '__main__':
    app.run()
