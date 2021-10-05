from datetime import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

from peewee import *

db = SqliteDatabase('timeapp.db')

class User(UserMixin, Model):
    '''
    User class, inherits from flask_login.UserMixin and peewee.Model
    Containes username and hashed password of user
    '''
    username = CharField(unique=True)
    password = CharField(max_length=100)
    checked_in = BooleanField(default=False)

    #Peewee Model requirements
    class Meta():
        database = db

    @classmethod
    def create_user(cls, username, password):
        try:
            cls.create(
                username=username,
                password=generate_password_hash(password)
            )
        except IntegrityError:
            pass

class CheckIn(Model):
    '''
    CheckIn class, inherits from flask_login.Model
    Contains timeIn, and timeOutInfo
    '''

    timeIn = DateTimeField(default=datetime.now)
    timeOut = DateTimeField(null=True)
    user = ForeignKeyField(
            User,
            related_name='checkins'
    )

    def check_out(self):
        self.timeOut = datetime.now()
        self.save(only=[User.timeOut])

    class Meta():
        database = db
        #Order by most recent timeIn
        order_by = ('-timeIn')

def initialize():
    db.connect()
    db.create_tables([User, CheckIn], safe=True)
