from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message

from datetime import datetime
import os
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)
mail = Mail(app)

app.config['SECRET_KEY'] = '###fdf32D34fg!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] ='smtp@gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_USERNAME'] = 'col.jops@gmail.com'
#app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_PASSWORD'] = 'gerst67^!'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class NameForm(FlaskForm):
    name = StringField('Jak masz na imię?', validators=[DataRequired()])
    submit = SubmitField('Wyślij')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' %self.name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self) -> str:
        return '<User %r>' %self.username

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        #old_name = session.get('name')
        user = User.query.filter_by(username=form.name.data).first()
        #if old_name is not None and old_name != form.name.data:
        if user is None:
            """
            flash('Wygląda na to, że teraz nazywasz się inaczej ;)')
            return redirect(url_for('index'))
            """
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['know'] = False
        else:
            session['know'] = True
        name = form.name.data
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('user', name=name))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), know=session.get('know', False))

@app.route('/user/<name>')
def user(name):
    user_agent = request.headers.get('User-Agent')
    return render_template('user.html', name=name, user_agent=user_agent)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )