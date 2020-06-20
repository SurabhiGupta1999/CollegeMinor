import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_bcrypt import Bcrypt
from forms import SignUpForm, LoginForm, ForgotForm, ComplaintForm


engine = create_engine("postgres://liscgjktgvoiid:e44ad379dfcc1fce6ed0f3de28c59077c899252c7fe094565383de810e598d80@ec2-52-86-73-86.compute-1.amazonaws.com:5432/d2uiio9chcha1n")
db = scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = '123minor456project789'


@app.route('/', methods=['GET', 'POST'])
def index():

    a_email = session.get('aemail')
    if a_email:
        return redirect(url_for('admin'))

    stud_email = session.get('semail')
    if stud_email:
        return redirect(url_for('student'))

    form = SignUpForm()

    if form.validate_on_submit():
        id = form.id.data
        fname = form.fname.data
        email = form.email.data
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        contactno = form.contactno.data
        design = form.design.data

        info = db.execute("SELECT * FROM admininfo WHERE email = :email", {"email": email }).fetchone()
        info_one = db.execute("SELECT * FROM studentinfo WHERE email = :email", {"email": email }).fetchone()


        if info:
            flash('This Email ID already registered with us. Please use another email id to register.')
            return redirect(url_for('index'))
        elif design == "admin":
            db.execute("INSERT INTO admininfo (id, fname, email, password, contactno, designation) VALUES (:id, :fname, :email, :password, :contactno, :designation)", {'id' : id, 'fname' : fname, 'email' : email, 'password' : hash_password, 'contactno' : contactno, 'designation' : design})
            db.commit()
        elif info_one:
            flash('This Email ID already registered with us. Please use another email id to register.')
            return redirect(url_for('index'))
        elif design == "stud":
            db.execute("INSERT INTO studentinfo (id, fname, email, password, contactno, designation) VALUES (:id, :fname, :email, :password, :contactno, :designation)", {'id' : id, 'fname' : fname, 'email' : email, 'password' : hash_password, 'contactno' : contactno, 'designation' : design})
            db.commit()



        flash('Your Account has been successfully registered, you can now Login.')

        return redirect(url_for('index'))

    return render_template('index.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        design = form.design.data
        info = db.execute("SELECT * FROM admininfo WHERE email = :email", {"email": email }).fetchone()
        info_one = db.execute("SELECT * FROM studentinfo WHERE email = :email", {"email": email }).fetchone()



        if design == "admin":
            if info and bcrypt.check_password_hash(info.password, password) is True:
                session['aemail'] = info.email
                return redirect(url_for('admin'))
            else:
                flash('You have entered incorrect Email ID or Password, please enter correct Email ID and Password')
                return redirect(url_for('login'))
        if design == "stud":
            if info_one and bcrypt.check_password_hash(info_one.password, password) is True:
                session['semail'] = info_one.email
                return redirect(url_for('student'))
            else:
                flash('You have entered incorrect Email ID or Password, please enter correct Email ID and Password')
                return redirect(url_for('login'))



    return render_template('login.html', form=form)



@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('semail', None)
    session.pop('aemail', None)


    return redirect(url_for('index'))


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()

    if form.validate_on_submit():
        email = form.email.data
        design = form.design.data

    return render_template('forgotpass.html', form=form)



@app.route('/admin', methods=['GET', 'POST'])
def admin():

    return render_template('admin.html')



@app.route('/student', methods=['GET', 'POST'])
def student():

    stud_email = session.get('semail')

    form = ComplaintForm()

    if form.validate_on_submit():
        fname = form.fname.data
        email = form.email.data
        date = form.date.data
        degree = form.degree.data
        semester = form.semester.data
        complaintcategory = form.complaintcategory.data
        message = form.message.data
        #file = form.file.data

        db.execute("INSERT INTO complain (fname, email, date, degree, semester, complaintcategory, message) VALUES (:fname, :email, :date, :degree, :semester, :complaintcategory, :message)", {'fname' : fname, 'email' : email, 'date' : date, 'degree' : degree, 'semester' : semester, 'complaintcategory' : complaintcategory, 'message' : message})
        db.commit()

        flash('Complaint Registered Successfully.')

        return redirect(url_for('student'))


    return render_template('student.html', form=form)


@app.route('/complainthistory', methods=['GET', 'POST'])
def complainthistory():

    stud_email = session.get('semail')

    complaintdetail = db.execute("SELECT * FROM complain WHERE email = :email", {'email' : stud_email}).fetchall()


    return render_template('complainthistory.html', complaintdetail=complaintdetail)


@app.route('/studprofileupdate', methods=['GET', 'POST'])
def studprofileupdate():

    stud_email = session.get('semail')

    studinfo = db.execute("SELECT * FROM studentinfo WHERE email = :email", {'email' : stud_email}).fetchone()
