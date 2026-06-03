from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileAllowed, FileRequired

# 🧍 Register Form
class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

# 🔑 Login Form
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

# 🧾 Checkout Form
class CheckoutForm(FlaskForm):
    address = StringField("Address", validators=[DataRequired(), Length(min=5, max=200)])
    city = StringField("City", validators=[DataRequired(), Length(min=2, max=50)])
    pincode = StringField("Pincode", validators=[DataRequired(), Length(min=4, max=10)])
    submit = SubmitField("Place Order")

# 🎨 Custom Cake Order Form
class CustomOrderForm(FlaskForm):
    message = TextAreaField("Message / Special Request", validators=[DataRequired(), Length(max=300)])
    image = FileField("Upload Cake Design", validators=[
        FileRequired(),
        FileAllowed(["jpg", "jpeg", "png"], "Images only!")
    ])
    submit = SubmitField("Submit Custom Order")
