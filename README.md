#CheckIn App
A basic timetracking program, built using Python, Flask, and a SQLite databse using Peewee as an ORM 

##General Info
I wrote this project to get more experience with [Flask](https://flask.palletsprojects.com/en/2.0.x/), [Peewee](https://docs.peewee-orm.com/en/latest/), and wtf_forms. It provides basic timeTracking functionality, allowing you to checkin/checkout and see the time spent in each individual session. 

##Technologies
Created using 
* Flask 2.0.1
* Peewee 3.14.4
* WTForms 2.3.3
* bcrypt 3.2.0

##Setup 
'shell
$ git clone https://github.com/rmcclorey/TimeTracker
$ pip install -r requirements.txt
$ python src/app.py
'

##TODO
* Create a better view for list of times. 
* Create better tools for viewigng aggregate time. 
* Add names/categories for what activity is being tracked. 
* Filter times based on categories. 
