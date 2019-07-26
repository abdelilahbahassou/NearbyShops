"""
This is where the views are defined for Flask
"""

from flask import Flask, request, render_template, redirect, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from flask_login import login_required, current_user, login_user, logout_user


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/SingedUp', methods = ['POST', 'GET'])
def SignedUp():
    
    if request.method == 'POST':
        
        email = request.form.get('em')
        name = request.form.get('fn')
        password = request.form.get('pass1')
    
        user = User.query.filter_by(email=email).first() 
        #check if a use with the same email exists
        if user: 
            flash('Email address already exists')
            return redirect(url_for('index'))

        # create new user with a hashed password
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        flash('You are now registred, please log in..')
    return render_template("index.html")



@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('em')
    password = request.form.get('pass')

    user = User.query.filter_by(email=email).first()
    print(user)
    # check if user exists, and check his credentials 
    if not user or not check_password_hash(user.password, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('index')) # if user doesn't exist or password is wrong, redirect to index

    # if everything is fine, the user then should be redirected to his account
    login_user(user)
    return redirect(url_for('shops'))



@app.route('/shops', methods=["POST","GET"])
@login_required
def shops():
    
    selected = ""
    #get all shops
    shops = Shop.query.order_by(Shop.id.desc()).all()
    shopsByDistance = Shop.query.order_by(Shop.ShopDistance).all()
    
    #get the current user
    user = User.query.filter_by(email=current_user.email).first()
    #get shops liked /disliked by the current user
    shops_liked_by_user = user.liked
    shops_disliked_by_user = user.disliked
    #get shops not liked by the user to show them in home (liked/disliked shops should not appear in home)
    shops_to_show = [shop for shop in shops if (shop not in shops_liked_by_user) and (shop not in shops_disliked_by_user)]
    shops_to_show_dist = [shop for shop in shopsByDistance if (shop not in shops_liked_by_user) and (shop not in shops_disliked_by_user)]
    select = request.form.get('sortBy')
    if select == "distance":
        shops_to_show = shops_to_show_dist
        selected = 'selected'
        
    if shops_to_show == []:
        flash("No shops to show at the moment ...")
    return render_template('Logged.html', shops = shops_to_show, selected = selected, user = user.name)

#this view perfoms actions of liking or disliking and redirects to home
@app.route('/liked', methods=["POST"])
@login_required
def liked_disliked():
    Shop_in = request.form.get("ShopName")
    user = User.query.filter_by(email=current_user.email).first()
    print(request.form.get('like'))
    if request.form.get('action') == "Like":
        lshop = Shop.query.filter_by(ShopName=Shop_in).first()
        user.liked.append(lshop)
        db.session.commit()
        flash('Shop liked')
        return redirect(url_for('shops'))
    elif request.form.get('action') == "disLike":
        dshop = Shop.query.filter_by(ShopName=Shop_in).first()
        user.disliked.append(dshop)
        db.session.commit()
        flash('shop disliked')
        return redirect(url_for('shops'))
    return redirect(url_for('shops'))

# this view shows the page of liked shops
@app.route('/likedShops')
@login_required
def likedShops():
    
    user = User.query.filter_by(email=current_user.email).first()
    shops_liked_by_user = user.liked
    shops_disliked_by_user = user.disliked

    shops_to_show = [shop for shop in shops_liked_by_user if shop not in shops_disliked_by_user]
    
    if shops_to_show == []:
        flash("You haven't liked any shops yet.")
    return render_template('LikedShops.html', shops = shops_to_show, user = user.name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)