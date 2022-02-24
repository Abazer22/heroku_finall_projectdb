from pickle import FALSE, TRUE
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Malak2014$@localhost/final_project'
    
else:
    
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tnqxvigfiejndi:80a371c8f1bbf17a746c55bac908d51b36e851d6ab375a8e66fb7b70ebde57d2@ec2-35-153-35-94.compute-1.amazonaws.com:5432/d5l8ib0pjcjo9u'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback1'
    id = db.Column(db.Integer, primary_key=True)
    teacher = db.Column(db.String(200), unique=True)
    student = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, teacher, student, rating, comments):
        self.teacher = teacher
        self.student = student
        self.rating = rating
        self.comments = comments



#@app.route('/')
#def hello_world():
   # return 'Hello world'

# Use flask_pymongo to set up mongo connection

@app.route("/")
def index():
   
   return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        teacher = request.form['teacher']
        student = request.form['student']
        rating = request.form['rating']
        comments = request.form['comments']
        #print(teacher, student, rating, comments)

        if teacher == '' or student == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.teacher == teacher).count() == 0:
            data = Feedback(teacher, student, rating, comments)
            db.session.add(data)
            db.session.commit()
            
            return render_template('success.html')
        return render_template('index4.html', message='You have already submitted feedback')   

if __name__ == "__main__":
   app.run()

   