from flask import request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user, login_user, logout_user
from flask_mail import Message
from app import app, mail, db
from main.forms import *
from main.models import Project, admin_required, User
from . import page


def send_email(to, subject, template, **kwargs):
    msg = Message("[MyResume]" + subject, recipients=[to])
    msg.body = template
    mail.send(msg)

@page.before_request
def before_request():
    if request.headers.get('X-Forwarded-Proto') == "http":
        url = request.url.replace("http", "https", 1)
        return redirect(url)



@page.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    projects = Project.query.all()
    num_projects = len(projects)
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        send_email("hoanghm4@gmail.com", name, message + " " + email)
        return redirect(url_for("page.form_submitted"))
    return render_template('index.html', form=form, projects=projects, num_projects=num_projects, resume_link=app.config["RESUME_LINK"], submitted=False)

@page.route('/submitted', methods=['GET', 'POST'])
def form_submitted():
    form = ContactForm()
    projects = Project.query.all()
    num_projects = len(projects)
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        send_email("hoanghm4@gmail.com", name, message + " " + email)
        return redirect(url_for("page.form_submitted"))
    return render_template('index.html', form=form, projects=projects, num_projects=num_projects, resume_link=app.config["RESUME_LINK"], submitted=True)

@page.route('/projects/<id>', methods=['GET', 'POST'])
def project(id):
    project = Project.query.get_or_404(id)
    form = ContactForm()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        send_email("hoanghm4@gmail.com", name, message + " " + email)
        return redirect(url_for("page.project"))
    return render_template('project_base.html', form=form, project=project, resume_link=app.config["RESUME_LINK"], submitted=False)

@page.route('/add_project', methods=['GET', 'POST'])
@login_required
@admin_required
def add_project():
    form = AddProjectForm()
    if request.method == "POST":
        title = request.form['title']
        image_link = request.form['image_link']
        short_description = request.form['short_description']
        content = request.form['content']
        new_project = Project(title=title, image_link=image_link, short_description=short_description, content=content)
        db.session.add(new_project)
        db.session.commit()
        new_project_id = Project.query.filter_by(title=title).first().id
        return redirect(url_for('page.project', id=new_project_id))
    return render_template('add_project.html', form=form)

@page.route('/edit_project/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(id):
    form = AddProjectForm()
    project = Project.query.get_or_404(id)
    if request.method == "POST":
        project.title = form.title.data
        project.image_link = form.image_link.data
        project.short_description = form.short_description.data
        project.content = form.content.data
        db.session.commit()
        return redirect(url_for('page.project', id=id))
    else:
        form.title.data = project.title
        form.image_link.data = project.image_link
        form.short_description.data = project.short_description
        form.content.data = project.content
    return render_template('add_project.html', form=form, project=project)

@page.route('/delete_project/<id>', methods=['GET'])
@login_required
@admin_required
def delete_project(id):
    cur_project = Project.query.get_or_404(id)
    db.session.delete(cur_project)
    db.session.commit()
    return redirect(url_for('page.index'))


@page.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cur_user = User.query.filter_by(username=form.username.data).first()
        if cur_user is not None and cur_user.verify_password(form.password.data):
            login_user(cur_user)
            return redirect(url_for('page.index'))
        else:
            flash('Wrong username or password.')
            return redirect(url_for('page.login'))
    return render_template('login.html', form=form)

@page.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('page.index'))

@page.route('/change_password', methods=['GET', 'POST'])
@login_required
@admin_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_pw = form.old_pw.data
        new_pw = form.new_pw.data
        confirm_pw = form.confirm_pw.data
        if current_user.verify_password(old_pw):
            if new_pw != confirm_pw:
                flash('Passwords do not match.')
                return redirect(url_for('page.change_password'))
            current_user.password = new_pw
            db.session.commit()
            flash('Password changed successfully!')
            return redirect(url_for('page.index'))
        else:
            flash('Wrong password.')
            return redirect(url_for('page.change_password'))
    return render_template('change_password.html', form=form)

@page.route('/<anything>')
def error_404(anything):
    return "<h1> Hey! Nothing to find here. </h1> "