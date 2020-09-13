from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import required, Email


class AddProjectForm(Form):
    title = StringField(validators=[required()], label='Title')
    image_link = StringField(validators=[required()], label='Project Image Link')
    short_description = TextAreaField(validators=[required()], label='Short Description')
    content = TextAreaField(validators=[required()], label='Content')
    submit = SubmitField(label="Add Project")

class EditProjectForm(Form):
    title = StringField(validators=[required()], label='Title')
    image_link = StringField(validators=[required()], label='Project Image Link')
    short_description = TextAreaField(validators=[required()], label='Short Description')
    content = TextAreaField(validators=[required()], label='Content')
    submit = SubmitField(label="Save changes")

class ContactForm(Form):
    name = StringField( validators=[required()])
    email = StringField(validators=[required(), Email()])
    message = TextAreaField(validators=[required()])
    submit = SubmitField(label="Send Inquiry")


class LoginForm(Form):
    username = StringField(validators=[required()])
    password = PasswordField(validators=[required()])
    submit = SubmitField(label='Log In')


class ChangePasswordForm(Form):
    old_pw = PasswordField(validators=[required()])
    new_pw = PasswordField(validators=[required()])
    confirm_pw = PasswordField(validators=[required()])
    submit = SubmitField(label='Change Password')