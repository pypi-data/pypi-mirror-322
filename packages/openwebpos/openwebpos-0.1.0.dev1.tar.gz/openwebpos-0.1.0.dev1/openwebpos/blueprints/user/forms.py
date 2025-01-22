from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

placeholder = {"placeholder": " "}


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired()], render_kw=placeholder
    )
    password = PasswordField(
        "Password", validators=[DataRequired()], render_kw=placeholder
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In", render_kw={"class": "btn tonal"})
