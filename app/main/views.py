from datetime import datetime
from flask import render_template, session, redirect, url_for, request
from . import main
from . forms import NameForm
from .. import db
from .. models import User

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