#!/usr/bin/env python3
import string
import random
import json
from functools import wraps
from flask import Flask, render_template, request, redirect
from flask import url_for, jsonify, flash
from flask import session as login_session
from flask import make_response
from database_setup import Category, Item
from database_setup import session
from auth import google_connect, google_disconnect, get_user_id

# Create an instance of the class Flask
# with the name of the running app as the argument '__name__'
app = Flask(__name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Authenticaltion - check if user is logged-in
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")

            return redirect('/login')
    return decorated_function


# Create a state token to prevent request forgery
# Store it in the session for later validation
@app.route('/login')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # Render the login template
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    """Connects to google account"""
    return google_connect()


@app.route('/gdisconnect')
def gdisconnect():
    """Disconnects from google account"""
    return google_disconnect()


# Root
@app.route('/')
def show_catalog():
    """Show all catalog categories and items
    """

    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('catalog.html', categories=categories, items=items)


# JSON endpoint
@app.route('/catalog.json')
def catalog_json():
    """Return list of categories and items in each category
    """

    categories = session.query(Category).all()
    catalog = []

    # iterate over categories and format them
    for c in categories:
        items = session.query(Item).filter_by(category_id=c.id)
        c = c.serialize
        c['Item'] = [i.serialize for i in items]

        catalog.append(c)

    return jsonify(Category=catalog)


@app.route('/catalog/<category_name>/<item_name>.json')
def item_json(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(category_id=category.id,
                                         name=item_name).one()
    result = {}
    result['Item'] = item.serialize
    return jsonify(result)


# Show category with items
@app.route('/catalog/<category_name>/items/')
def show_category(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id=category.id)
    categories = session.query(Category).all()
    return render_template('catalog.html', items=items, categories=categories)


# Show description
@app.route('/catalog/<category_name>/<item_name>/')
def show_item_description(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Item).filter_by(name=item_name,
                                         category_id=category.id).one()
    return render_template('itemdescription.html', item=item)


# Edit an item
@app.route('/catalog/<category_name>/<item_name>/edit',
           methods=['GET', 'POST'])
@login_required
def edit_item(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    edited_item = session.query(Item).filter_by(name=item_name,
                                                category_id=category.id).one()

    # Authorisation - check if current user can edit the item
    # Only a user who created an item can edit/delete it
    user_id = get_user_id(login_session['email'])
    if edited_item.user_id != user_id:
        message = json.dumps('You are not allowed to edit the item')
        response = make_response(message, 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Post method
    if request.method == 'POST':
        if request.form['name']:
            edited_item.name = request.form['name']
        if request.form['description']:
            edited_item.description = request.form['description']
        if request.form['category']:
            category = session.query(Category).filter_by(name=request.form
                                                         ['category']).one()
            edited_item.category = category

        session.add(edited_item)
        session.commit()
        return redirect(url_for('show_category',
                                category_name=edited_item.category.name))
    else:
        categories = session.query(Category).all()
        return render_template('edititem.html', item=edited_item,
                               categories=categories)


# Delete item
@app.route('/catalog/<category_name>/<item_name>/delete',
           methods=['GET', 'POST'])
@login_required
def delete_item(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item_to_delete = session.query(Item).filter_by(name=item_name,
                                                   category=category).one()

    # Authorisation - check if current user can edit the item
    # Only a user who created an item can edit/delete it
    user_id = get_user_id(login_session['email'])
    if item_to_delete.user_id != user_id:
        message = json.dumps('You are not allowed to delete the item')
        response = make_response(message, 403)
        response.headers['Content-Type'] = 'application/json'
        return response

    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        return redirect(url_for('show_category',
                                category_name=category.name))

    else:
        return render_template('deleteitem.html', item=item_to_delete)


# Add an item
@app.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def add_item():
    categories = session.query(Category).all()
    if request.method == 'POST':
        new_item = Item(
            name=request.form['name'],
            description=request.form['description'],
            category=session.query(Category).
            filter_by(name=request.form['category']).one(),
            user_id=login_session['user_id'])

        session.add(new_item)
        session.commit()

        return redirect(url_for('show_catalog'))
    else:
        return render_template('additem.html', categories=categories)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
