from flask_wtf import Form
from wtforms import TextField, PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.

class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=3, max=40)]
    )

class JobForm(Form):
    title = TextField(
        'Title', validators=[DataRequired(), Length(min=1, max=40)]
    )

    database = RadioField(
        'Database', choices=[('vertica','Vertica'),('mysql','MySQL')]
    )

    host = TextField(
        'Host', validators=[DataRequired(), Length(min=1, max=40)]
    )

    username = TextField(
        'Username', validators=[DataRequired(), Length(min=1, max=40)]
    )

    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=1, max=40)]
    )    

    spreadsheet = TextField(
        'Spreadsheet', validators=[DataRequired(), Length(min=1, max=40)]
    )

    sheet = TextField(
        'Sheet', validators=[DataRequired(), Length(min=1, max=40)]
    )

    query = TextAreaField(
        'Query'
    )

    schedule = TextField(
        'Schedule', validators=[DataRequired(), Length(min=1, max=40)]
    )