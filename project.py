from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from flask import session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import secret_key
import categories_methods  # Category database methods
import books_methods  # Book database methods
import login_methods  # User database methods

app = Flask(__name__)


# Facebook login
@app.route('/login')
def showLogin():
    ''' Method to display login page
    '''
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    '''Execute logging in with Facebook
    '''
    if request.args.get('state') != session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/oauth/access_token?grant_type'
        '=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token))
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # splitting off the expire tag from token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    session['provider'] = 'facebook'
    session['username'] = data["name"]
    session['email'] = data["email"]
    session['facebook_id'] = data["id"]

    stored_token = token.split("=")[1]
    session['access_token'] = stored_token

    # Users picture
    url = ('https://graph.facebook.com/v2.4/me/picture?'
        '%s&redirect=0&height=200&width=200' % token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    session['picture'] = data["data"]["url"]
    user = login_methods.compareUsers(session)

    output = ''
    output += '<h4 class="white-text center-align">'
    if user:
        output += 'Welcome Back, '
    else:
        output += 'Welcome, '
    output += session['username']

    output += '!</h4>'
    output += '<img src="'
    output += session['picture']
    output += ' " class="circle profile-circle"> '
    output += '<div class="progress">'
    output += '<div class="indeterminate"></div>'
    output += '</div>'

    flash("Now logged in as %s" % session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    ''' Disconnect from Facebook and clear session
    '''
    facebook_id = session['facebook_id']
    access_token = session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    session.clear()  # clear session
    flash("Successfully logged out")
    return redirect(url_for('showCategories'))

# JSON APIs


@app.route('/categories/<int:category_id>/books/JSON')
def categoriesBooksJSON(category_id):
    ''' JSON for books belonging to a single category

        Args:
            category_id = the id of the category
    '''
    books = books_methods.booksByID(category_id)
    return jsonify(Books=[b.serialize for b in books])


@app.route(
    '/categories/<int:category_id>/books/<int:book_id>/JSON')
def categoriesBooksJSON(category_id, book_id):
    ''' JSON for a single book

        Args:
            category_id = the id of the category
            book_id = the id of the book
    '''

    book = books_methods.booksFromID(book_id)
    return jsonify(Book=book.serialize)


@app.route('/categories/JSON')
def categoriesBooksJSON():
    ''' JSON for all categories

    '''
    categories = categories_methods.categoriesQuery()
    return jsonify(Categories=[c.serialize for c in categories])

# Categories


@app.route('/')
@app.route('/categories/')
def showCategories():
    ''' Main page for showing all Categories of books

    '''
    categories = categories_methods.categoriesQuery()
    return render_template('categories.html',
                           categories=categories, session=session)


@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    ''' Create a new Category

    '''
    if request.method == 'POST':
        user = login_methods.getUserBySession(session)
        if user:  # Checks for a logged in user
            name = request.form['name']
            user_id = user.id
            categories_methods.newCategory(name, user_id)
            flash("Successfully created new category %s" % name)
            return redirect(url_for('showCategories'))
        else:
            flash("Log in to create a Category")
            return redirect(url_for('showLogin'))
    else:
        return render_template('newcategories.html')


@app.route('/categories/<int:categories_id>/edit', methods = ['GET', 'POST'])
def editCategory(categories_id):
    ''' Edit a Category

        Args:
            categories_id = The id of the category

    '''
    category=categories_methods.categoryByID(categories_id)
    user=login_methods.getUserBySession(session)
    if request.method == 'POST':
        name=request.form['name']
        if user:  # Checks for a logged in user
            # Checks to see if user is author of category or admin
            if user.id == category.user_id or user.administrator is True:
                if name != category.name and name:
                    categories_methods.editCategory(category, name)
                    flash("Successfully edited %s" % name)
                    return redirect(url_for('showCategories'))
                else:
                    flash("Sorry you didn't change anything")
                    return render_template('editcategories.html',
                                           category = category)
            else:
                flash("user is not author of the category")
                return render_template('editcategories.html',
                                       category=category)
        else:
            flash("Sorry only logged in users can edit")
            return redirect(url_for('showLogin'))
    else:
        return render_template('editcategories.html', category=category)


@app.route('/categories/<int:categories_id>/delete', methods=['GET', 'POST'])
def delCategory(categories_id):
    ''' Delete a Category

        Args:
            categories_id = The id of the category
    '''
    category = categories_methods.categoryByID(categories_id)
    user = login_methods.getUserBySession(session)

    if request.method == 'POST':
        if user: # Checks for logged in user
            # Checks if user is author of category or admin
            if user.id == category.user_id or user.administrator is True:
                categories_methods.delCategory(category)
                flash("Successfully deleted %s" % category.name)
                return redirect(url_for('showCategories'))
            elif user:
                flash("Sorry you are not authorized to delete this Category")
                return render_template('delcategories.html', category=category)
            else:
                flash("Sorry only logged in users can delete")
                return redirect(url_for('showLogin'))
        else:
            flash("Sorry only logged in users can delete")
            return redirect(url_for('showLogin'))
    else:
        return render_template('delcategories.html', category=category)


# Books
@app.route('/categories/<int:categories_id>/')
@app.route('/categories/<int:categories_id>/books/')
def showBooks(categories_id):
    ''' Show all Books belonging to a Category

        Args:
            categories_id = The id of the category
    '''
    books = books_methods.booksByID(categories_id)
    category = categories_methods.categoryByID(categories_id)
    return render_template('books.html',
                           category=category, books=books)


@app.route('/categories/<int:categories_id>/books/new',
           methods=['GET', 'POST'])
def newBook(categories_id):
    ''' Create a new Book

        Args:
            categories_id = The id of the category
    '''
    category = categories_methods.categoryByID(categories_id)
    user = login_methods.getUserBySession(session)
    if request.method == 'POST':
        if user: # Checks for logged in user
            title = request.form['title']
            isbn = request.form['isbn']
            url = request.form['image']
            author = request.form['author']
            description = request.form['description']
            user_id = user.id
            books_methods.newBook(
                category.id, title, isbn, url, author, description, user_id)
            flash("Successfully created new Book %s" % title)
            return redirect(url_for('showBooks',
                                    categories_id=category.id))
        else:
            flash("Sorry only logged in users can create new books")
            return redirect(url_for('showLogin'))
    else:
        return render_template('newbooks.html', category=category)


@app.route('/categories/<int:categories_id>/books/<int:book_id>/edit',
           methods=['GET', 'POST'])
def editBook(categories_id, book_id):
    ''' Edit a Book

        Args:
            categories_id = The id of the category
            book_id = The id of the book
    '''
    book = books_methods.bookFromID(book_id)
    user = login_methods.getUserBySession(session)
    if request.method == "POST":
        if user.id == book.user_id or user.administrator is True:
            if request.form['title'] != book.title:
                book.title = request.form['title']
            if request.form['isbn'] != book.isbn:
                book.isbn = request.form['isbn']
            if request.form['image'] != book.image:
                book.image = request.form['image']
            if request.form['author'] != book.author:
                book.author = request.form['author']
            if request.form['description'] != book.description:
                book.description = request.form['description']
            books_methods.editBook(book)
            flash("Successfully edited %s" % book.title)
            return redirect(url_for('showBooks',
                                    categories_id=categories_id,
                                    book_id=book_id))
        elif user:
            flash("Sorry you are not authorized to edit this book")
            return render_template('editbooks.html', book=book)
        else:
            flash("Sorry only logged in users can edit")
            return redirect(url_for('showLogin'))
    else:
        return render_template('editbooks.html', book=book)


@app.route('/categories/<int:categories_id>/books/<int:book_id>/delete',
           methods=['GET', 'POST'])
def delBook(categories_id, book_id):
    ''' Delete a Book

        Args:
            categories_id = The id of the category
            book_id = The id of the book
    '''
    book = books_methods.bookFromID(book_id)
    user = login_methods.getUserBySession(session)
    if request.method == 'POST':
        if user.id == book.user_id or user.administrator is True:
            books_methods.delBook(book)
            flash("Successfully deleted book")
            return redirect(url_for('showBooks',
                                    categories_id=categories_id))
        elif user:
            flash("Sorry you are not authorized to delete this book")
            return render_template('delbooks.html', book=book)
        else:
            flash("Sorry only logged in users can delete")
            return redirect(url_for('showLogin'))
    else:
        return render_template('delbooks.html', book=book)


@app.route('/categories/<int:categories_id>/books/<int:book_id>/checkout',
           methods=['GET', 'POST'])
def checkOutBook(categories_id, book_id):
    ''' Check out a book from the library

        Args:
            categories_id = The id of the category
            book_id = The id of the book
    '''
    book = books_methods.bookFromID(book_id)
    user = login_methods.getUserBySession(session)
    if request.method == 'POST':
        if user:
            books_methods.checkOutBook(book, user.id)
            flash("Successfully checked out %s" % book.title)
            return redirect(url_for('showBooks',
                                    categories_id=categories_id))
        else:
            flash("Sorry only logged in users can checkout books")
            return redirect(url_for('showLogin'))
    else:
        return render_template('checkoutbooks.html',
                               categories_id=categories_id, book=book)

# Check in a Book.


@app.route('/categories/<int:categories_id>/books/<int:book_id>/checkin',
           methods=['GET', 'POST'])
def checkInBook(categories_id, book_id):
    ''' Check in a book from the library

        Args:
            categories_id = The id of the category
            book_id = The id of the book
    '''
    book = books_methods.bookFromID(book_id)
    user = login_methods.getUserBySession(session)
    lastcheckout = books_methods.lastCheckout(book.id)
    if request.method == 'POST':
        if user.id == lastcheckout.user_id or user.administrator is True:
            books_methods.checkInBook(book, user.id)
            flash("Successfully checked in %s" % book.title)
            return redirect(url_for('showBooks',
                                    categories_id=categories_id))
        elif user:
            flash("Sorry chap you can't check this in")
            return render_template('checkinbooks.html',
                                   categories_id=categories_id, book=book)
        else:
            flash("Sorry only logged in users can checkin books")
            return redirect(url_for('showLogin'))
    else:
        return render_template('checkinbooks.html',
                               categories_id=categories_id, book=book)

# User Page


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def userPage(user_id):
    ''' Show user information

        Args:
            Show users information
    '''
    user = login_methods.getUserByID(user_id)  # The user being changed
    editor = login_methods.getUserBySession(session)  # The user editing
    if request.method == 'POST':
        if editor.id == int(session['facebook_id']) \
                or editor.administrator is True:
            if request.form['name'] != user.name:
                user.name = request.form['name']
                # For test only, delete on production
                # Will change user to admin if nickname changed to Admin
                if request.form['name'] == "Admin":
                    user.administrator = True
            if request.form['email'] != user.email:
                user.email = request.form['email']
            checked = 'admin' in request.form
            ischecked = bool(checked)
            if ischecked != user.administrator \
                    and editor.administrator is True:
                user.administrator = ischecked
            login_methods.editUser(user)
            flash("Successfully edited %s" % user.name)
            return redirect(url_for('showCategories'))
        else:
            flash("Sorry you don't have authorization to edit this user")
            return redirect(url_for('showCategories'))
    else:
        if user.id == int(session['facebook_id']) \
                or editor.administrator is True:
            return render_template('user.html', user=user, editor=editor)
        else:
            flash("Sorry you don't have authorization to access this user")
            return redirect(url_for('showCategories'))


@app.route('/user/<int:user_id>/delete')
def deleteUser(user_id):
    '''Deletes a user from the database

    Args:
        user_id = The id of the user to delete

    '''
    user = login_methods.getUserByID(user_id)
    editor = login_methods.getUserBySession(session)
    if editor.administrator is True:
        login_methods.deleteUser(user)
        flash("%s deleted" % user.name)
        return redirect(url_for('adminConsole'))
    else:
        flash("Only admins can delete users!")
        return redirect(url_for('showCategories'))


@app.route('/user/admin', methods=['GET', 'POST'])
def adminConsole():
    '''Admin console to see all users and make changes

    '''
    admin = login_methods.getUserBySession(session)
    if admin.administrator is True:
        users = login_methods.queryUsers()
        return render_template('admin.html', users=users)
    else:
        flash("Sorry only admins have access to this page")
        return redirect(url_for('showCategories'))


# Run app
if __name__ == '__main__':
    app.secret_key = secret_key.key  # If testing enter your own secret key
    app.debug = True
    app.run(host='0.0.0.0', port=8500)
