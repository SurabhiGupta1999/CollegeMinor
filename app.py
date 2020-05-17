import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_bcrypt import Bcrypt
from forms import SignUpForm, LoginForm, ForgotForm


engine = create_engine("postgres://liscgjktgvoiid:e44ad379dfcc1fce6ed0f3de28c59077c899252c7fe094565383de810e598d80@ec2-52-86-73-86.compute-1.amazonaws.com:5432/d2uiio9chcha1n")
db = scoped_session(sessionmaker(bind=engine))


app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = '123minor456project789'


@app.route('/', methods=['GET', 'POST'])
def index():

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
            flash('This Email ID already registered with us.')
            return redirect(url_for('index'))
        else:
            db.execute("INSERT INTO admininfo (id, fname, email, password, contactno, designation) VALUES (:id, :fname, :email, :password, :contactno, :designation)", {'id' : id, 'fname' : fname, 'email' : email, 'password' : hash_password, 'contactno' : contactno, 'designation' : design})
            db.commit()
        if info_one:
            flash('This Email ID already registered with us.')
            return redirect(url_for('index'))
        else:
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
            if info and bcrypt.check_password_hash(info.password, password):
                return redirect(url_for('admin'))
            else:
                flash('You have entered incorrect Email ID or Password, please enter correct Email ID and Password')
                return redirect(url_for('login'))
        if design == "stud":
            if info_one and bcrypt.check_password_hash(info.password, password):
                return redirect(url_for('admin'))
            else:
                flash('You have entered incorrect Email ID or Password, please enter correct Email ID and Password')
                return redirect(url_for('login'))



    return render_template('login.html', form=form)


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
