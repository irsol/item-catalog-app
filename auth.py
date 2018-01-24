import requests
import json
from flask import request
from flask import session as login_session
from flask import make_response
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from database_setup import User
from database_setup import session


# Json with credentials
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

APPLICATION_NAME = "Item Catalog Application"


def create_user(login_session):
    """ User helper functions
        Creates a new user in our db
    """
    new_user = User(name=login_session['username'],
                    email=login_session['email'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user_info(user_id):
    """ Returns user object assoccieted with id number,
        if user id passed into the method
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def get_user_id(email):
    """ Takes an email and reterns an id, if email belongs to a user
        stored inour db
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Google login
def google_connect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='',
                                             redirect_uri='postmessage')
        # oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'
    url = url.format(access_token)
    # Create Get request containing the URL and access token

    result = requests.get(url).json()

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['picture'] = data['picture']

    # Check if user exists, if it doesn't create a new one
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    # Response thet knows user's name and return their pictura
    html = """
        <h1>Welcome, {name}!</h1>
        <img src="{picture}" style = "width: 300px;
            height: 300px; border-radius: 150px;
            -webkit-border-radius: 150px;-moz-border-radius: 150px;">
    """.format(name=login_session['username'],
               picture=login_session['picture'])

    return html


# DISCONNECT - Revoke a current user's token and reset their login_session
def google_disconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])

    # Revoke access token
    result = requests.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': login_session['access_token']},
                           headers={'content-type':
                                    'application/x-www-form-urlencoded'})

    print('result is ')
    print(result)

    # Reset users session since otherwise it won't be possible to
    # logout and login
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

    if result.status_code == 200:
        # Reset the user's session
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        message = json.dumps('Failed to revoke token for given user.')
        response = make_response(message, 400)
        response.headers['Content-Type'] = 'application/json'
        return response
