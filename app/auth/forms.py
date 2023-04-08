from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Length(1,64), Email()])
    password = StringField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')