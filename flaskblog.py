from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secretkey44"
#SqlAlchemy Database Configuration w/ MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/crud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#model table for CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    identify = db.Column(db.String(100))
    points = db.Column(db.String(100))
    def __init__(self, name, identify, points):

        self.name = name
        self.identify = identify
        self.points = points

#index route
@app.route('/')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", students = all_data)

#route for inserting data to the mysql db via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        identify = request.form['identify']
        points = request.form['points']
        my_data = Data(name, identify, points)
        db.session.add(my_data)
        db.session.commit()
        flash("Student Inserted")
        return redirect(url_for('Index'))
 
 
#update route for updating student data
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.identify = request.form['identify']
        my_data.points = request.form['points']
        db.session.commit()
        flash("Student Updated")
        return redirect(url_for('Index'))

#route for deleting student
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted")
    return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)