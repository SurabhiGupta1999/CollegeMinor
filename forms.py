from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,SubmitField, PasswordField, RadioField, SubmitField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class SignUpForm(FlaskForm):
    id = StringField('ID*', validators=[DataRequired()])
    fname = StringField('Full Name*', validators=[DataRequired()])
    email = EmailField('Email ID*',validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    contactno = TelField('Mobile No*.', validators=[DataRequired(), Length(min=10, max=10)])
    design = SelectField(u'Designation*', choices=[('admin', 'Admin'), ('stud', 'Student')], validators=[DataRequired()])
    submit = SubmitField('Sign Up >>')


class LoginForm(FlaskForm):
    email = EmailField('Email ID*',validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    design = SelectField(u'Designation*', choices=[('admin', 'Admin'), ('stud', 'Student')], validators=[DataRequired()])
    submit = SubmitField('Login >>')


class ForgotForm(FlaskForm):
    email = EmailField('Email ID*',validators=[DataRequired(), Email()])
    design = SelectField(u'Designation*', choices=[('admin', 'Admin'), ('stud', 'Student')], validators=[DataRequired()])
    submit = SubmitField('Change your Password')
