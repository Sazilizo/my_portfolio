from app import db , login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    user_id =db.Column(db.Integer, db.ForeignKey('profile.id'), nullable=True, index=True)
    user = db.relationship("Profile", backref='user_id', lazy=True,
                           foreign_keys=[user_id])
    def __repr__(self):
        return "User('{}', {}, {})".format(self.username,
                                self.email, self.image_file)

 

class Profile(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    first = db.Column(db.String(20), nullable=False)
    last = db.Column(db.String(20), nullable=False)
    identification = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(3), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    suburb = db.Column(db.String(50), nullable=False)
    street = db.Column(db.String(50), nullable=False)
    street_number = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow )
    about_user = db.Column(db.Text, nullable=False)
    about_business = db.Column(db.Text, nullable=False)
    business_plan = db.Column(db.String(30), nullable=False)
    profile_id =db.Column(db.Integer, db.ForeignKey('user.id',use_alter=True, name='profile_id'), nullable=False)
    user = db.relationship("User", backref='profile', lazy=True,
                           foreign_keys=[User.user_id])

    def __repr__(self):
        return "User('{}', {})".format(self.first,self.last)
