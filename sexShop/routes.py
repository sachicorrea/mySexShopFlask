from sexShop import app
from flask import render_template, redirect, url_for, flash, request
from sexShop.models import Item, User
from sexShop.forms import RegisterForm, LoginForm, PurchaseItemForm
from sexShop import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Felicitaciones. Usted ha comprado {p_item_object.name} por {p_item_object.price}", category="success")
            else:
                flash(f"Desafortunadamente no tienes el suficiente saldo para comprar {p_item_object.name}", category="danger")
        return redirect(url_for('market_page'))
    
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        return render_template('market.html', items=items, purchase_form=purchase_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'La cuenta fue creada satisfactoriamente. Ahora estas conectado como {user_to_create.username}', category='success')

        return redirect(url_for('market_page'))

    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'Hubo un error creando el usuario: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Exitoso! Está conectado como: {attempted_user.username} ', category='success')
            return redirect(url_for('market_page'))

        else:
            flash('Nombre de usuario o contraseña no están registrados. Intente nuevamente', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("Has sido deslogueado", category='info')
    return redirect(url_for("home_page"))
