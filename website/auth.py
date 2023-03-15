from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email)<4:
            flash("Email must be greater than 4 characters",category='error')
        elif len(name)<2:
            flash("Name should be greater than 2 character",category='error')

        elif password1!=password2:
            flash("Password didnot match",category='error')
            
        elif len(password1)<7:
            flash("Password must contain 7 characters",category='error')
        
        else:
            new_user = User(email=email,name=name,password=generate_password_hash(password2,method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('Account Created!',category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html")