import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_bcrypt import Bcrypt
from forms import SignUpForm, LoginForm, ForgotForm, ComplaintForm, changepassword, complaint_status


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


    a_email = session.get('aemail')
    if a_email:
        return redirect(url_for('admin'))

    stud_email = session.get('semail')
    if stud_email:
        return redirect(url_for('student'))


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

    a_email = session.get('aemail')
    if a_email:
        return redirect(url_for('admin'))

    stud_email = session.get('semail')
    if stud_email:
        return redirect(url_for('student'))


    form = ForgotForm()

    if form.validate_on_submit():
        email = form.email.data
        design = form.design.data

        info = db.execute("SELECT * FROM admininfo WHERE email = :email", {"email": email }).fetchone()
        info_one = db.execute("SELECT * FROM studentinfo WHERE email = :email", {"email": email }).fetchone()

        print(form.email.data)


        if design == "admin":
            if info:
                session['fpemailOne'] = info.email
                session['ades'] = "admin"
                return redirect(url_for('change_password'))
            else:
                flash(f'Sorry, your email does not exist, please check again.', 'danger')
                return redirect(url_for('forgot'))
        if design == "stud":
            if info_one:
                session['fpemailTwo'] = info_one.email
                session['sdes'] = "stud"
                return redirect(url_for('change_password'))
            else:
                flash(f'Sorry, your email does not exist, please check again.', 'danger')
                return redirect(url_for('forgot'))


    return render_template('forgotpass.html', form=form)



@app.route('/change_password', methods=['GET', 'POST'])
def change_password():


    a_email = session.get('aemail')
    if a_email:
        return redirect(url_for('admin'))

    stud_email = session.get('semail')
    if stud_email:
        return redirect(url_for('student'))


    fpemailOne = session.get('fpemailOne')
    fpemailTwo = session.get('fpemailTwo')
    ades = session.get('ades')
    sdes = session.get('sdes')


    cp = changepassword()

    if cp.validate_on_submit():
        password = cp.password.data

        if ades and fpemailOne is not None:
            chpa_info = db.execute("SELECT * from admininfo WHERE email = :email AND designation = :design", {"email" : fpemailOne, "design" : ades}).fetchone()
            if chpa_info:
                if bcrypt.check_password_hash(chpa_info.password, password) is True:
                    flash(f'please try a different password, this is your current password', 'danger')
                    return redirect(url_for('change_password'))
                else:
                    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    db.execute("UPDATE admininfo SET password = :password WHERE email = :email", {"password" : hash_password , "email" : fpemailOne })
                    flash(f'Your Password has been changed successfully, you can now login.', 'success')
                    db.commit()

                    return redirect(url_for('login'))

        elif sdes and fpemailTwo is not None:
            chpa_infoone = db.execute("SELECT * from studentinfo WHERE email = :email AND designation = :design", {"email" : fpemailTwo, "design" : sdes}).fetchone()
            if chpa_infoone:
                if bcrypt.check_password_hash(chpa_infoone.password, password) is True:
                    flash(f'please try a different password, this is your current password', 'danger')
                    return redirect(url_for('change_password'))
                else:
                    hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
                    db.execute("UPDATE studentinfo SET password = :password WHERE email = :email", {"password" : hash_password , "email" : fpemailTwo })
                    flash(f'Your Password has been changed successfully, you can now login.', 'success')
                    db.commit()

                    return redirect(url_for('login'))



    return render_template('changepassword.html', cp=cp)


@app.route('/admin', methods=['GET', 'POST'])
def admin():

    stud_complain = db.execute("SELECT * FROM complain").fetchall()



    return render_template('admin.html', stud_complain=stud_complain)


@app.route('/display_complaint/<int:complaint_id>', methods=['GET', 'POST'])
def display_complaint(complaint_id):


    return  render_template('display_complaint.html')




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



    return render_template('stud_my_profile.html', studinfo=studinfo)
