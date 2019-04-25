#!/usr/bin/env/python3

"""
Udacity Full-Stack Web Developer Nanodegree
Homework 2 : Catalog Items App
Student: Chin H. Seah
"""

from flask import Flask, render_template, request, redirect, jsonify, url_for,\
    flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Base, Category, CategoryItem, User, CatItem
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import logging

app = Flask(__name__)

# logging.basicConfig(level=logging.DEBUG)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

categories = session.query(Category).all()


@app.route('/')
@app.route('/catalog')
def show_catalog():
    """
    Display list of categories and latest category items.
    """
    numberOfCategories = len(categories)
    latestItems = get_latest_items(numberOfCategories)
    return render_template('index.html',
                           categories=categories,
                           latestItems=latestItems)


@app.route('/catalog.json')
def catalog_json():
    catalog = [c.serialize for c in categories]
    for cat in catalog:
        catItems = get_category_items(cat["category_id"])
        items = [ci.serialize for ci in catItems]
        if len(items) > 0:
            cat["Item"] = items
    return jsonify(Category=catalog)


@app.route('/catalog/categories.json')
def catagories_json():
    return jsonify(Category=[c.serialize for c in categories])


@app.route('/catalog/<int:category_id>/items.json')
def catagory_items_json(category_id):
    catItems = [ci.serialize for ci in get_category_items(category_id)]
    for item in catItems:
        item["category_id"] = category_id
    return jsonify(Item=catItems)


@app.route('/catalog/<int:category_id>/item/<int:item_id>/item.json')
def catagory_item_json(category_id, item_id):
    itemObj = get_category_item(category_id, item_id)
    if itemObj is None:
        itemObj = {}
    else:
        itemObj = itemObj.serialize
        itemObj["category_id"] = category_id
    return jsonify(Item=itemObj)


@app.route('/catalog/<category>/items')
def show_category_items(category):
    """
    Display list of categories and items for selected category.
    """
    catId = get_category_id(category)
    itemsCount = 0
    items = []
    if catId is None:
        flash("Category %s not found!" % (category))
    else:
        categoryitems = get_category_items(catId)
        if categoryitems is not None:
            itemsCount = len(categoryitems)
            for item in categoryitems:
                newItem = CatItem(catId, category, item.name)
                items.append(newItem)

    if itemsCount == 1:
        categoryTotal = "1 item"
    else:
        categoryTotal = "%d items" % (itemsCount)
    return render_template('index.html', categoryName=category,
                           categories=categories,
                           categoryTotal=categoryTotal,
                           latestItems=items)


@app.route('/catalog/<category>/<item>')
def show_category_item(category, item):
    """
    Display item description
    """
    authorized = False
    catId = get_category_id(category)
    if catId is None:
        flash("Category %s not found!" % (category))
        return redirect(url_for('show_catalog'))
    else:
        itemId = get_item_id(catId, item)
        if itemId is None:
            flash("Item %s not found!" % (item))
            itemObj = CategoryItem(name=item, description="Unknown.")
        else:
            itemObj = get_category_item(catId, itemId)
            # If user was original creator then authorized to edit or delete
            if 'username' in login_session and \
               login_session['user_id'] == itemObj.user_id:
                authorized = True
    return render_template('itemdetails.html',
                           categoryName=category,
                           item=itemObj,
                           authorized=authorized)


@app.route('/catalog/<category>/<item>/delete', methods=['GET', 'POST'])
def delete_category_item(category, item):
    """
    Delete a category item
    """
    if 'username' not in login_session:
        return redirect('/login')

    catId = get_category_id(category)
    if catId is None:
        flash("Category %s not found!" % (category))
        return redirect(url_for('show_catalog'))
    else:
        itemId = get_item_id(catId, item)
        if itemId is None:
            flash("Item %s not found!" % (item))
            return redirect(url_for('show_catalog'))
        else:
            itemToDelete = get_category_item(catId, itemId)
            if itemToDelete.user_id != login_session['user_id']:
                return "<script>function myFunction() \
                        {alert('You are not authorized to delete this item. \
                        Please select your own item to delete.');}\
                        </script><body onload='myFunction()'>"
            if request.method == 'POST':
                session.delete(itemToDelete)
                flash('%s Successfully Deleted' % itemToDelete.name)
                session.commit()
                return redirect(url_for('show_category_items',
                                        category=category))
            else:
                return render_template('itemdelete.html',
                                       categoryName=category,
                                       item=itemToDelete)


@app.route('/catalog/new', methods=['GET', 'POST'])
def new_category_item():
    """
    Create a new category item into Catalog
    """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = CategoryItem(
            name=request.form['name'],
            description=request.form['description'],
            user_id=login_session['user_id'],
            category_id=request.form['category'])
        logging.debug("New Item: %s %s %s %s", newItem.name,
                      newItem.description, str(newItem.user_id),
                      str(newItem.category_id))
        session.add(newItem)
        flash('New Item %s Successfully Added.' % newItem.name)
        session.commit()
        return redirect(url_for('show_catalog'))
    else:
        return render_template('newitem.html', categories=categories)


@app.route('/catalog/<category>/items/new', methods=['GET', 'POST'])
def add_category_item(category):
    """
    Add a new category item into Catalog
    """
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        catId = get_category_id(category)
        newItem = CategoryItem(
            name=request.form['name'],
            description=request.form['description'],
            user_id=login_session['user_id'],
            category_id=catId)
        logging.debug("New Item: %s %s %s %s", newItem.name,
                      newItem.description, str(newItem.user_id),
                      str(newItem.category_id))
        session.add(newItem)
        flash('New Item %s Successfully Added.' % newItem.name)
        session.commit()
        return redirect(url_for('show_category_items', category=category))
    else:
        return render_template('newcategoryitem.html',
                               categoryName=category,
                               categories=categories)


@app.route('/catalog/<category>/<item>/edit', methods=['GET', 'POST'])
def edit_category_item(category, item):
    """
    Edit a category item
    """
    if 'username' not in login_session:
        return redirect('/login')

    catId = get_category_id(category)
    if catId is None:
        flash("Category %s not found!" % (category))
        return redirect(url_for('show_catalog'))
    else:
        itemId = get_item_id(catId, item)
        if itemId is None:
            flash("Item %s not found!" % (item))
            return redirect(url_for('show_category_items', category=category))
        else:
            itemToEdit = get_category_item(catId, itemId)
            if itemToEdit.user_id != login_session['user_id']:
                return "<script>function myFunction() \
                        {alert('You are not authorized to edit this item. \
                        Please select your own item to edit.');}\
                        </script><body onload='myFunction()'>"
            if request.method == 'POST':
                itemToEdit.name = request.form['name']
                itemToEdit.description = request.form['description']
                itemToEdit.category_id = request.form['category']
                logging.debug("itemToEdit %s %s %s %s", itemToEdit.name,
                              itemToEdit.description, str(itemToEdit.user_id),
                              str(itemToEdit.category_id))
                session.add(itemToEdit)
                session.commit()
                flash('Item Successfully Edited.')
                if itemToEdit.category_id != catId:
                    flash('Item Category Changed.')
                return redirect(url_for('show_category_items',
                                category=category))
            else:
                return render_template('edititem.html',
                                       categoryName=category,
                                       categories=categories,
                                       item=itemToEdit)


@app.route('/login')
def showLogin():
    """
    Display login screen and create anti-forgery state token
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    logging.debug("Login session state %s", state)
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        logging.debug("State not equal")
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        logging.debug("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
                    json.dumps('Current user is already connected.'),
                    200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = get_user_id(data["email"])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
        150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    logging.info("done!")
    return output


# User Helper Functions
def create_user(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/disconnect')
def disconnect():
    """
    Disconnect based on provider
    """
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['google_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('show_catalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('show_catalog'))


def get_category_id(name):
    """
    Get category identifier by its name.
    """
    cat = session.query(Category).filter_by(name=name).first()
    if cat is None:
        return None
    return cat.id


def get_category_items(categoryId):
    """
    Get category items by its identifier.
    """
    return session.query(CategoryItem).\
        filter_by(category_id=categoryId).\
        order_by(CategoryItem.name).all()


def get_category_item(categoryId, itemId):
    """
    Get category item by its identifier.
    """
    return session.query(CategoryItem).filter_by(id=itemId).\
        filter_by(category_id=categoryId).first()


def get_item_id(categoryId, name):
    """
    Get item identifier by its name.
    """
    item = session.query(CategoryItem).filter_by(name=name).\
        filter_by(category_id=categoryId).first()
    if item is None:
        return None
    return item.id


def get_latest_items(itemLimit):
    """
    Get list of latest category items with limit for number
    of items. Name of item has category in parenthesis.
    """
    items = []

    for c, ci in session.query(Category, CategoryItem).\
            filter(Category.id == CategoryItem.category_id).\
            order_by(CategoryItem.create_date.desc())[0:itemLimit]:
        newItem = CatItem(ci.id, c.name, ci.name)
        items.append(newItem)

    # for debugging
    # for i in items:
    #    print(i)
    return items


if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
