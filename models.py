"""
This is where the DB is created, and models are defined ...
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin
from flask_login import LoginManager 


# config:
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.app_context().push()
db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#----------------- models ------------------

likedshops = db.Table('likedshops',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('shop_id', db.Integer, db.ForeignKey('shop.id'))
                     )
dislikedshops = db.Table('disliked',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('shop_id', db.Integer, db.ForeignKey('shop.id'))
                        )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    liked = db.relationship("Shop", secondary=likedshops, backref=db.backref('likedby', lazy='dynamic'))
    disliked = db.relationship("Shop", secondary=dislikedshops, backref=db.backref('dislikedby', lazy='dynamic'))
    
class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    ShopName = db.Column("ShopName", db.String(100), unique=True)
    ShopDesc = db.Column("ShopDesc", db.String(100))
    ShopDistance = db.Column("ShopDistance", db.Integer)
    ShopImage = db.Column("ShopImage", db.String(1000))

#---------------- init database after adding tables ----------------
def init_db():
    global db
    db.create_all(app=app)

if __name__ == '__main__':
    init_db()