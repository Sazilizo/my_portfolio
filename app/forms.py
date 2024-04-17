from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField,TextAreaField
from wtforms.validators import data_required, Length, Email, EqualTo, ValidationError
from app.models import User

class Register(FlaskForm):
    username = StringField("Username", validators=[data_required(), Length(min=6, max=20)])
    email = StringField("Email", validators=[data_required(), Email()])
    password = PasswordField("Password", validators=[data_required(), Length(min=8, max=20)])
    password_valid =PasswordField("confirm passowrd", validators=[data_required(), EqualTo("password")])
    submit = SubmitField("Sign up")
    
    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists, choose another one")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("email already exists, choose another one")

class UpdateUserProfile(FlaskForm):
    username = StringField("Username", validators=[data_required(), Length(min=6, max=20)])
    email = StringField("Email", validators=[data_required(), Email()])
    profile_picture = FileField("Update profile pictures", validators=[FileAllowed(['jpeg', 'jpg', 'png'])])#FileSize(min_size=100266, max_size=1000000)
    submit = SubmitField('Update')
    
    def validate_user(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists, choose another one")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("email already exists, choose another one")


class RegisterProfile(FlaskForm):
    first = StringField("First", validators=[data_required(), Length(min=2, max=70)])
    last = StringField("Last", validators=[data_required(), Length(min=2, max=70)])
    gender = StringField("Gender (m/f)",  validators=[data_required(), Length(min=1, max=3)])
    identification = StringField("Id/Passport", validators=[data_required(), Length(min=13, max=70)])
    country = StringField("Country", validators=[data_required(), Length(min=2, max=70)])
    province = StringField("Province/State", validators=[data_required(), Length(min=2, max=70)])
    city = StringField("City", validators=[data_required(), Length(min=2, max=70)])
    suburb = StringField("Suburb", validators=[data_required(), Length(min=2, max=70)])
    street = StringField("Street", validators=[data_required(), Length(min=2, max=70)])
    street_number = IntegerField("Street Number", validators=[data_required()])
    about_user = TextAreaField("About you", validators=[data_required(), Length(min=200, max=370)])
    about_business = TextAreaField("About your business", validators=[data_required(), Length(min=200, max=370)])
    business_plan = FileField("Business Plan", validators=[FileAllowed(['pdf','jpg', 'jpeg', 'png'])])
    submit = SubmitField('Submit')
    
    
class Login(FlaskForm):
    email = StringField("Email", validators=[data_required(), Email()])
    password = PasswordField("Password", validators=[data_required(), Length(min=8, max=20)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log in")