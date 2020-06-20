from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,SubmitField, PasswordField, RadioField, MultipleFileField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField, TelField, DateField
from wtforms.validators import DataRequired, Email, Length, InputRequired

class SignUpForm(FlaskForm):
    id = StringField('ID*', validators=[DataRequired()])
    fname = StringField('Full Name*', validators=[DataRequired()])
    email = EmailField('Email Id*',validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    contactno = TelField('Mobile No*.', validators=[DataRequired(), Length(min=10, max=10)])
    design = SelectField(u'Designation*', choices=[('admin', 'Admin'), ('stud', 'Student')], validators=[DataRequired()])
    submit = SubmitField('Sign Up >>')


class LoginForm(FlaskForm):
    email = EmailField('Email Id*',validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    design = SelectField(u'Designation*', choices=[('admin', 'Admin'), ('stud', 'Student')], validators=[DataRequired()])
    submit = SubmitField('Login >>')


class ForgotForm(FlaskForm):
    email = EmailField('Email Id*',validators=[DataRequired(), Email()])
    design = SelectField(u'Designation*', choices=[('admin', 'Admin'), ('stud', 'Student')], validators=[DataRequired()])
    submit = SubmitField('Change your Password')



class ComplaintForm(FlaskForm):
    fname = StringField('Full Name *', validators=[DataRequired()])
    email = EmailField('Email Id*',validators=[DataRequired(), Email()])
    date = DateField('Date', validators=[DataRequired()])
    degree = SelectField(u'Degree*', choices=[('bachelors', 'Bachelors'), ('masters', 'Masters')], validators=[DataRequired()])
    semester = SelectField(u'Semester*', choices=[('first', 'First'), ('second', 'Second'), ('third', 'Third'), ('fourth', 'Fourth'), ('fifth', 'Fifth'), ('sixth', 'Sixth'), ('seventh', 'Seventh'), ('eighth', 'Eighth')], validators=[DataRequired()])
    complaintcategory = SelectField(u'Complant Category*', choices=[('infrastructure', 'Infrastructure'), ('accounts', 'Accounts'), ('academics', 'Academics'), ('management', 'Management'), ('faculty', 'Faculty'), ('library', 'Library')], validators=[DataRequired()])
    message = TextAreaField('Enter Complaint Details', validators=[DataRequired(), Length(max=100)])
    #file = MultipleFileField(u'Upload File')
    submit = SubmitField('Submit')
