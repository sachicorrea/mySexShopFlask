from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from sexShop.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                'Nombre de usuario ya existe! Intente con un nombre de usuario diferente')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(
            email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError(
                'El email ingresado ya existe! Intente un email diferente')

    username = StringField(label='Nombre de Usuario:', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email:', validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label='Contraseña:', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirmar Contraseña:', validators=[
                              EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Crear Cuenta')


class LoginForm(FlaskForm):
    username = StringField(label='Nombre de Usuario:',
                           validators=[DataRequired()])
    password = PasswordField(label='Contraseña:', validators=[DataRequired()])
    submit = SubmitField(label='Ingresar')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label="Comprar producto")

class SellItemForm(FlaskForm):
    submit = SubmitField(label="Vender producto")


