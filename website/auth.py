from flask import Blueprint,render_template, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_wtf import FlaskForm
from wtforms import SelectField,StringField,DateField, EmailField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import login_user, login_required, logout_user, current_user
from datetime import date


auth = Blueprint('auth', __name__)

class AdminForm(FlaskForm):
    name = StringField("Username",validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Login Admin")

class AdminSignUpForm(FlaskForm):
    name = StringField("Username", validators=[DataRequired(), Length(min=2)])
    password_1 = PasswordField('Password', validators=[DataRequired()])
    password_2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password_1')])
    submit= SubmitField("Create Admin")

class LogForm(FlaskForm):
    email = EmailField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Login User")

class SignUpForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2)])
    surname = StringField("Surname",validators=[DataRequired(), Length(min=2)])
    email = EmailField("Email",validators=[DataRequired(), Email()])
    password_1 = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password_1')])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Create Account")

class UpdateForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2)])
    surname = StringField("Surname",validators=[DataRequired()])
    email = EmailField("Email",validators=[DataRequired(), Email()])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Update Account")

class SelectInsuranceForm(FlaskForm):
    insurance_choices = [('Car Insurance'), ('House Insurance'), ('Life Insurance')]
    insurance_name = SelectField("Insurance", choices=insurance_choices, validators=[DataRequired()])
    amount = IntegerField("Insurance Amount CZK", validators=[DataRequired()])
    creation_date = DateField("Commencement date", validators=[DataRequired()])
    expiration_date = DateField("Expiration date",  validators=[DataRequired()])
    submit = SubmitField("Create Insurance")    

    def validate_creation_date(self, field):
        if field.data < date.today():
            raise ValidationError('The insurance effective date cannot be earlier than today\'s date.')

    def validate_expiration_date(self, field):
        if field.data <= self.creation_date.data:
            raise ValidationError('The insurance expiration date cannot be earlier than the insurance effective date.')
        
        
@auth.route('/admin_user', methods = ['GET','POST'])
def admin_login():
    loginform = AdminForm()

    if loginform.validate_on_submit():
        username = loginform.name.data
        password = loginform.password.data

        admin = User.query.filter_by(name=username).first()
        if admin:
            if check_password_hash(admin.password, password):
                flash('Logged in successfully',category='success')
                login_user(admin, remember=False)#keeps in cookies to rememners user is logged in
                return redirect(url_for('views.admin'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("admin/admin_login.html", user=current_user, loginform = loginform)


#"""Creating a route with methods so it can be used from login html"""
@auth.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LogForm()

    if loginform.validate_on_submit():
        email = loginform.email.data
        password = loginform.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully',category='success')
                login_user(user, remember=False)
                return redirect(url_for('views.home_page'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("authorize/login.html", user=current_user, loginform = loginform)#if we have logged in our user, we can use this template

@auth.route('/logout')
@login_required # this decorator is used to prevent to see logged out for not login users
def logout():
    logout_user()
    return redirect(url_for('views.home_page'))




@auth.route('/admin_sign_up', methods=['GET','POST'])
def admin_signup():
    form = AdminSignUpForm()

    if form.validate_on_submit():
        username = form.name.data
        password = form.password_1.data
        
        admin = User.query.filter_by(name=username).first()
        
        if admin:
            flash("Username already exists!", category='error')
        else:
            new_admin=User(name=username,password=generate_password_hash(password, method='sha256'))
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin, remember=True)
            flash("Admin created!",category='success')
            return redirect(url_for('views.admin'))
        
    return render_template("admin/sign_up_admin.html", form=form, admin=current_user)


@auth.route('/sign_up', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    
    if form.validate_on_submit():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password_1.data
        address = form.address.data

        user = User.query.filter_by(email=email).first()
        
        if user:
            flash("Email already exists!", category='error')
        else:
            new_user= User(name=name,surname=surname,email=email,password=generate_password_hash(password, method='sha256'),address=address)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!",category='success')
            return redirect(url_for('views.home'))
        
    return render_template("authorize/sign_up.html", form=form, user=current_user)