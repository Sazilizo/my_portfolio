from app import app, bcrypt, db, UPLOAD_FOLDER
from app.forms import Register, Login, UpdateUserProfile, RegisterProfile
from app.models import User, Profile
from flask import Blueprint,request, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
import secrets
import os
from PIL import Image
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf'}
bp = Blueprint("routes",__name__)


@bp.route("/")
@bp.route("/home")
def home():
    return render_template("home.html")

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user= User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("account created for {}! ".format(form.username.data), 'success')
        return redirect(url_for("routes.login"))
    return render_template("register.html", title="Sign up", form=form)
    
    
@bp.route("/login" , methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("routes.home"))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email= form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                next_page = 'routes.'+next_page
                return redirect(url_for(next_page))
            return redirect(url_for("routes.account"))
        flash("login unsuccessful. Please check email and password! ", "danger")
        # return redirect(url_for("routes.login"))accout
    return render_template("login.html", title="log in", form=form)


def save_profile_picture(form_picture):
    rand_name = secrets.token_hex(8)
    file_name, file_ext = os.path.splitext(form_picture.filename)
    picture_filen = rand_name + file_ext
    picture_path = os.path.join(app.root_path, 
                                'static/pictures', picture_filen)
    
    Image.open(form_picture).thumbnail((125,125)).save(picture_path)

    return picture_filen
  
  
@bp.route("/account" , methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserProfile()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_profile_picture(form.profile_picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account successfully update", "success")
        return redirect(url_for("routes.account"))
    image_file = url_for('static', filename='pictures/'+current_user.image_file)
    return render_template("account.html", image_file=image_file, form=form)


def file_upload(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("Not an allowed file extension")
            return redirect(url_for("routes.profile"))
    file = request.files['file']
    if file.filename == '':
        flash("No selected file")
        return redirect(url_for("routes.profile"))
    if file and file_upload(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for("uploaded_file", filename=filename))
    return filename
    
    
@bp.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    form = RegisterProfile()
    if form.validate_on_submit():
        if form.business_plan.data:
            business_file = file_upload(form.business_plan.data)
            current_user.business_plan = business_file
            file_upload
        user = Profile(first=form.first.data, last=form.last.data,
                       gender=form.gender.data,
                       identification=form.identification.data,
                       country=form.country.data,
                       province=form.province.data,
                       city=form.city.data, suburb=form.suburb.data,
                       street=form.street.data,
                       street_number=form.street_number.data,
                       about_user=form.about_user.data,
                       about_business=form.about_business.data)
        db.session.add(user)
        db.session.commit()
        flash("Your profile has been successfuly added", "success")
        return redirect(url_for("routes.home"))
    return render_template("profile.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("routes.home"))

