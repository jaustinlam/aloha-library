# from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Books, Users, CheckOut, CheckIn
# from flask import session # Use 'session' when referencing session data
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import datetime

# app = Flask(__name__)

# Create connection to database and start session
engine = create_engine('postgres://blejslzgodbfze:YmGABBtmbcP55dscnFEgAk66ES@ec2-107-21-248-129.compute-1.amazonaws.com:5432/d2qgb9ae9hbirv')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
sess = DBSession() # Use 'sess' when referencing database session

def booksByID(category_id):
    ''' All books belonging to a category

        Args:
            category_id = The id of the category

        Returns:
            All books that belong to given category in
            alphabetical order
    '''
    books = sess.query(Books).filter_by(category = category_id).order_by(asc(Books.title)).all()
    return books

def bookFromID(book_id):
    ''' Finds a single book from id number


        Args:
            The id of the book to find

        Returns:
            The book object
    '''
    book = sess.query(Books).filter_by(id = book_id).one()
    return book

def newBook(category_id, title, isbn, url, author, description, user_id):
    ''' Creates a new books

        Args:
            category_id = id of the category the book belongs to
            title = title of the book
            isbn = books isbn
            url = url of the image of the book
            author = the books author
            description = the books description
            user_id = the current user
    '''
    book = Books(
        title = title,
        image = url,
        description = description,
        author = author,
        isbn = isbn,
        category = category_id,
        user_id = user_id)
    sess.add(book)
    sess.commit()

def editBook(book):
    ''' Adds and commits edits to a book

        Args:
            book: the book to be edited
    '''
    sess.add(book)
    print book.title
    sess.commit()


def delBook(book):
    '''Deletes a book from database

        Args:
            book = the book to delete
    '''
    sess.delete(book)
    sess.commit()

def checkOutBook(book, user_id):
    '''Enters a record that book was checked out
        Updates book record to show it is checkedout

        Args:
            book = the book to check out
            user_id = id of the user checking out the book
    '''
    book.checkedout = True
    checkout = CheckOut(
        book_id = book.id,
        user_id = user_id,
        date = datetime.datetime.now())
    sess.add(book)
    sess.add(checkout)
    sess.commit()

def checkInBook(book, user_id):
    '''Enters a record that book was checked in
        Updates book record to show it is checkedout

        Args:
            book_id = the book to check out
            user_id = the id of the user checking in.
    '''
    book.checkedout = False
    checkin = CheckIn(
        book_id = book.id,
        user_id = user_id,
        date = datetime.datetime.now())
    sess.add(book)
    sess.add(checkin)
    sess.commit()

def lastCheckout(book_id):
    '''Finds the most recent checkout record for a book

        Args:
            book_id = The id of the book

        Returns:
            The checkout record
    '''
    try:
        record = sess.query(CheckOut).filter_by(book_id = book_id).order_by(CheckOut.date.desc()).first()
        return record

    except:
        None





