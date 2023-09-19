from flask import Blueprint,render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Insurance
from . import db
from .auth import UpdateForm, SelectInsuranceForm

views = Blueprint('views',__name__)

@views.route('/', methods = ['GET','POST'])
def home_page():
    admin_exists = User.query.filter_by(id=1).first()
    return render_template("home.html", admin_exists=admin_exists)

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
    if current_user.id == 1:
        user_to_delete = User.query.get_or_404(id)
        try:
            db.session.delete(user_to_delete)
            db.session.commit()
            flash("User was deleted!", category='success')
            return redirect(url_for('views.admin'))
        except:
            flash("Something went wrong with deleting user!", category='error')
            return redirect(url_for('views.admin'))
    else:
        flash("You are not authorized to view this page! Please login as Admin", category='error')
        return redirect(url_for('auth.admin_login'))


@views.route('/my_account', methods =['GET','POST'])
@login_required
def my_account():
    user_table = User.query.filter_by(id=current_user.id).first()
    return render_template("user_info.html", current_user = current_user, table = user_table)

@views.route("/statistics/<int:id>", methods=['GET','POST'])
@login_required
def statistics(id):
    if current_user.id == 1:
        user = User.query.get(id)
        if user:
            user_insurances = user.insurance
            return render_template('statistics.html',id=id,user=user,user_insurances=user_insurances)
        else:
            flash("Error",category="error")
        return redirect(url_for('views.home'))
    else:
        flash("You are not authorized to view this page! Please login as Admin", category='error')
        return redirect(url_for('auth.admin_login'))


@views.route("/insurance_set/<int:id>", methods=['GET','POST'])
@login_required
def insurance_set(id):
    if current_user.id == 1:
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
            return redirect(url_for('views.admin'))
    else:
        flash("You are not authorized to view this page! Please login as Admin", category='error')
        return redirect(url_for('auth.admin_login'))
    

    return render_template('/admin/create_insurance.html', form=form, id=id)

# Update database record

@views.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
    if current_user.id == 1:
        form = UpdateForm()
        update_value= User.query.get_or_404(id)

        if form.validate_on_submit():
            update_value.name = form.name.data
            update_value.surname = form.surname.data
            update_value.email = form.email.data
            update_value.address = form.address.data
            try:
                db.session.commit()
                flash("User updated succesfully")
                return redirect(url_for("views.admin",form=form,update_value = update_value))
            except:
                flash("Error", category='error')
                return render_template("update.html",form= form, update_value = update_value)
            
        else:
            return render_template("/admin/update.html",id=id, form = form, update_value = update_value)
    else:
        flash("You are not authorized to view this page! Please login as Admin", category='error')
        return redirect(url_for('auth.admin_login'))       