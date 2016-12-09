# from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Books, Users, CheckOut, CheckIn
# import random
# import string
# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import FlowExchangeError
# import httplib2
# import json
# from flask import make_response
# import requests

# app = Flask(__name__)

# Create connection to database and start session
engine = create_engine('postgres://blejslzgodbfze:YmGABBtmbcP55dscnFEgAk66ES@ec2-107-21-248-129.compute-1.amazonaws.com:5432/d2qgb9ae9hbirv')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
sess = DBSession() # Use 'sess' when referencing database session

def categoriesQuery():
    ''' Query all Categories

        Returns:
            All categories

    '''
    categories = sess.query(Categories).order_by(Categories.name.asc())
    return categories

def categoryByID(category_id):
    ''' A single category by ID number

        Args:
            category_id = The id of the category

        Returns:
            A single catgory by id number
    '''
    category = sess.query(Categories).filter_by(id = category_id).one()

    return category


def newCategory(name, user_id):
    ''' Creates a new category

        Args:
            cname = The name of the new category
            user_id = The id of the user that created it
    '''
    category = Categories(
        name = name,
        user_id = user_id)
    sess.add(category)
    sess.commit()

def editCategory(category, name):
    ''' Edits a category

        Args:
            category = category to be edited
            name = new name for category
    '''
    category.name = name
    sess.add(category)
    sess.commit()

def delCategory(category):
    ''' Edits the name of category

        Args:
            category = The category object to be deleted
    '''
    sess.delete(category)
    sess.commit()









