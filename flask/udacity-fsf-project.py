from threading import get_ident
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Making an API Endpoint for all menu items of a restaurant (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItem=[i.serialize for i in items])

#Making an API Endpoint for one menu item (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)

@app.route('/')
@app.route('/restaurants/')
def allRestaurants():
    try:
        restaurants = session.query(Restaurant)
        return render_template('restaurant.html', restaurants=restaurants)
    except:
        return "no restaurant found"

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    try:
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        return render_template('menu.html', restaurant=restaurant, items=items)

    except:
        return "no result found for restaurant {}".format(restaurant_id)

# add a new menu item to an existing restaurant
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == "POST":
        newItem = MenuItem(name = request.form['name'], restaurant_id =
                           restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id =
                                restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id =
                               restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        new_name = request.form['new name']
        item.name = new_name
        session.add(item)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for('restaurantMenu', restaurant_id =
                                restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id =
                               restaurant_id, menu_id = menu_id, item=item)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/',
           methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        flash("menu item {} deleted!".format(item.name))
        return redirect(url_for('restaurantMenu', restaurant_id=
    restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=item)


if __name__ == '__main__':
    app.secret_key = "sec_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
