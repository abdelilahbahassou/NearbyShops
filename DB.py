"""
Useful function to manipulate CRUD actions
"""

from models import *

#add a new shop
def add_shop(suff):
    suff = str(suff)
    shopName = "shop_"+suff
    shopDesc = "An amazing Shop ..."
    shopDistance = int(suff)+20
    shopImage = "shopImages/shop"+suff+".jpg"
    
    shop = Shop.query.filter_by(ShopName=shopName).first() 
    
    if shop:
        print('shop with the same name is already added')
    else:
        new_shop = Shop(ShopName=shopName, ShopDesc = shopDesc, ShopDistance = shopDistance, ShopImage = shopImage)
        
        # add the new shop to the database
        db.session.add(new_shop)
        db.session.commit()
        print("shop successfully added")
# print all shops names
def get_all_shops():
    shops = Shop.query.all()
    return [shop.ShopName for shop in shops]

# delete a shop by name
def delete_shop():
    shop = Shop.query.filter_by(ShopName="shop_1").first()
    if shop:
        db.session.delete(shop)
        db.session.commit()
        print("shop deleted")
    else:
        print("something wrong happaned")

# get all shops liked by a user
def get_shops_liked_by_user():
    user1 = User.query.filter_by(email="abdou@abdou.com").first()
    print(user1.liked)

#get all users
def get_all_users():
    users = User.query.all()
    print([user.email for user in users])

#delete a user
def delete_user():
    user = User.query.filter_by(email="some@email")
    print(user)
    if user:
        db.session.delete(user)
        db.session.commit()
        print('user deleted')
    else:
        print('something went wrong :( ')

#empty a table
def empty_table():
    User.query.delete()
    #or
    #Shop.query.delete()
    
if __name__ == '__main__':

    # The a function here
    # or just perfomrs those action in an interactive Ipython console