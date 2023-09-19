from flask import Blueprint,render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Insurance
from . import db
from sqlalchemy import func
from .auth import InsuranceForm, UpdateForm, SelectInsuranceForm

# Creating a blueprint to usi it in __init__.py
views = Blueprint('views',__name__)

@views.route('/', methods = ['GET','POST'])
def home_page():
    return render_template("home.html", user=current_user)

@views.route('/my_account', methods =['GET','POST'])
@login_required
def home():
    user_table = User.query.filter_by(id=current_user.id).first()
    return render_template("user_info.html", user = current_user, table = user_table)

# Creating a route to admin page, wher you can do admin stuff
@views.route('/admin', methods = ['GET','POST'])
@login_required
def admin():
    if current_user.id == 1:
        all_users = User.query.all()
        return render_template('/admin/admin_tables.html', user_table = all_users, insurance_table = Insurance)
    else:
        flash("You are not authorized to view this page! Please login as Admin", category='error')
        return redirect(url_for('auth.admin_login'))


@views.route('/delete/<int:id>')
@login_required 
def delete_user(id):
    user_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User was deleted!", category='success')
        return redirect(url_for('views.admin'))
    except:
        flash("Something went wrong with deleting user!", category='error')
        return redirect(url_for('views.admin'))

@views.route("/statistics_global", methods=['GET','POST'])
def statistics_global():
    users_with_insurances = db.session.query(User, Insurance).join(
        User.insuranc).all()

    return render_template(
        'user_insurance_relationships.html',
        users_with_insurances=users_with_insurances
    )

@views.route("/statistics/<int:id>", methods=['GET','POST'])
def statistics(id):
    user = User.query.get(id)
    if user:
        user_insurances = user.insurance
        return render_template('statistics.html',id=id,user=user,user_insurances=user_insurances)
    else:
        flash("Error",category="error")
    return redirect(url_for('views.home'))

@views.route("/insurance_set/<int:id>", methods=['GET','POST'])
def insurance_set(id):
    form = SelectInsuranceForm()                                                                                                                                                                                            

    if form.validate_on_submit():
        selected_insurance_name = form.insurance_name.data
        amount = form.amount.data
        creation_date = form.creation_date.data
        expiration_date = form.expiration_date.data

        new_insurance = Insurance(insurance_name = selected_insurance_name, amount=amount, creation_date = creation_date, expiration_date = expiration_date)
        db.session.add(new_insurance)
        db.session.commit()
        

        user = User.query.get(id)
        user.insurance.append(new_insurance)    
        db.session.commit()

        flash("Insurance applied", category='success')


    return render_template('/admin/insurance_set.html', form=form, id=id)

@views.route('/insurance/', methods=['GET','POST'])
@login_required
def insurance_creation():
    form = InsuranceForm()
    all_insurances = Insurance.query.all()

    if current_user.id == 1:
        if form.validate_on_submit():
            insurance_name = form.insurance_name.data
        
            insurance = Insurance.query.filter_by(insurance_name=insurance_name).first()

            if insurance:
                flash("Insurance with this name already exists!", category='error')
            else:
                new_insurance=Insurance(insurance_name=insurance_name)
                db.session.add(new_insurance)
                db.session.commit()
                flash("Insurance created!")
                return redirect(url_for('views.admin'))
            
    return render_template("insurance.html", form = form, insurances = all_insurances )
# Update database record

@views.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form = UpdateForm()
    update_value= User.query.get_or_404(id)

    if form.validate_on_submit():
        update_value.name = form.name.data
        update_value.surname = form.surname.data
        update_value.email = form.email.data
        update_value.phone = form.phone.data
        update_value.address = form.address.data
        update_value.city = form.city.data
        update_value.postal_code = form.postal_code.data
        try:
            db.session.commit()
            flash("User updated succesfully")
            return redirect(url_for("views.admin",form=form,update_value = update_value))
        except:
            flash("Error", category='error')
            return render_template("update.html",form= form, update_value = update_value)
    
    else:
        return render_template("/admin/update.html",id=id, form = form, update_value = update_value)

