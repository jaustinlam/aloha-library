import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, ForeignKeyConstraint, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Categories(Base):
    ''' Class to represent Book Categories

        Args:
            Base
    '''
    __tablename__ = 'categories'

    name = Column(
        String(250), nullable = False)
    id = Column(
        Integer, primary_key = True)
    user_id = Column(
        Integer, ForeignKey('users.id'))
    users = relationship('Users')
    books = relationship('Books', cascade = 'all, delete-orphan')

    @property
    def serialize(self):
        return{
            'name'      :   self.name,
            'id'        :   self.id,
            'user_id'   :   self.user_id
        }


class Books(Base):
    ''' Class to represent individual Books

        Args:
            Base
    '''
    __tablename__ = 'books'

    title = Column(
        String(250), nullable = False)
    image = Column(
        String(250), nullable = False)
    description = Column(
        String(500))
    author = Column(
        String(80), nullable = False)
    isbn = Column(
        String(80), nullable = False)
    checkedout = Column(
        Boolean, default = False, nullable = False)
    id = Column(
        Integer, primary_key = True)
    category = Column(
        Integer, ForeignKey('categories.id'), nullable = False)
    user_id = Column(
        Integer, ForeignKey('users.id'), nullable = False)
    categories = relationship('Categories')
    users = relationship('Users')


    @property
    def serialize(self):
        return{
            'title'         :   self.title,
            'image'         :   self.image,
            'description'   :   self.description,
            'author'        :   self.author,
            'isbn'          :   self.isbn,
            'checkedout'    :   self.checkedout,
            'id'            :   self.id,
            'category'      :   self.category,
            'user_id'       :   self.user_id,
        }



class Users(Base):
    ''' Class to represent users

        Args:
            Base
    '''
    __tablename__ = 'users'

    name = Column(
        String(80), nullable = False)
    id = Column(
        Integer, primary_key = True)
    email = Column(
        String(80), nullable = False)
    administrator = Column(
        Boolean, default = False, nullable = False)

    @property
    def serialize(self):
        return{
            'name'          :   self.name,
            'id'            :   self.id,
            'email'         :   self.email,
            'administrator' :   self.administrator
        }



class CheckOut(Base):
    ''' Class to checked out items

        Args:
            Base
    '''
    __tablename__ = 'checkout'

    id = Column(
        Integer, primary_key = True)
    book_id = Column(
        Integer, ForeignKey('books.id'), nullable = False)
    user_id = Column(
        Integer, ForeignKey('users.id'), nullable = False)
    date = Column(
        DateTime)
    books = relationship(Books)
    users = relationship(Users)

    @property
    def serialize(self):
        return{
            'book_id'   :   self.book_id,
            'user_id'   :   self.user_id,
            'date'      :   self.date,
        }

class CheckIn(Base):
    ''' Class to checked in items

        Args:
            Base
    '''
    __tablename__ = 'checkin'

    id = Column(
        Integer, primary_key = True)
    book_id = Column(
        Integer, ForeignKey('books.id'), nullable = False)
    user_id = Column(
        Integer, ForeignKey('users.id'), nullable = False)
    date = Column(
        DateTime)
    books = relationship(Books)
    users = relationship(Users)

    @property
    def serialize(self):
        return{
            'book_id'   :   self.book_id,
            'user_id'   :   self.user_id,
            'date'      :   self.date,
        }

engine = create_engine(
    'postgres://blejslzgodbfze:YmGABBtmbcP55dscnFEgAk66ES@ec2-107-21-248-129.compute-1.amazonaws.com:5432/d2qgb9ae9hbirv')
Base.metadata.create_all(engine)
