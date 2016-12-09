from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Categories, Books, Users, CheckOut, CheckIn
from flask import session # Use 'session' when referencing session data
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

# Create connection to database and start session
engine = create_engine('sqlite:///librarydata.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
sess = DBSession() # Use 'sess' when referencing database session

def queryUsers():
    '''Query all Users

        returns:
            All Users

    '''
    users = sess.query(Users).all()
    return users

def getUserBySession(facebookuser):
    ''' Finds a user by session information

        Args:
            The session information

        Returns:
            The user or None
    '''
    try:
        x = sess.query(Users).filter_by(id = facebookuser['facebook_id']).one()
        return x
    except:
        None

def getUserByID(user_id):
    ''' Finds a user by id number

        Args:
            The session information

        Returns:
            The user or None
    '''
    try:
        x = sess.query(Users).filter_by(id = user_id).one()
        return x
    except:
        None



def compareUsers(facebookuser):
    '''Compares to see is user exists in database, else signs them up

        Args:
            facebookuser = The user information taken from the session

    '''
    user = getUserBySession(facebookuser)
    if user:
        return user
    else:
        createUser(facebookuser)
        user = getUserByID(facebookuser)




def createUser(facebookuser):
    ''' Creates a new user

        Args:
            facebookuser = the user information from the session

    '''
    newUser = Users(
                name = facebookuser['username'],
                id = facebookuser['facebook_id'],
                email = facebookuser['email'],
                administrator = False)
    sess.add(newUser)
    sess.commit()

def editUser(user):
    ''' Edits and commits a user

        Args:
            user = The user to be edited
    '''
    sess.add(user)
    sess.commit()

def deleteUser(user):
    '''Deletes a user from the database

        Args:
            user = the user to delete
    '''
    sess.delete(user)
    sess.commit()









