from multiprocessing import allow_connection_pickling
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wadood.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class wadood(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route("/", methods = ["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        obj = wadood(title = title, desc = desc)
        db.session.add(obj)
        db.session.commit()
    allObj = wadood.query.all()
    return render_template('index.html', allObj = allObj)


@app.route("/product")
def product():
    allObj = wadood.query.all()
    print(allObj)
    return "This is product page"

@app.route("/update/<int:sno>", methods = ["GET", "POST"])
def update(sno):
    if request.method =="POST":
        title = request.form['title']
        desc = request.form['desc']
        allObj = wadood.query.filter_by(sno=sno).first()
        allObj.title = title
        allObj.desc = desc
        db.session.add(allObj)
        db.session.commit()
        return redirect('/')
    allObj = wadood.query.filter_by(sno=sno).first()
    return render_template('update.html', allObj = allObj)

@app.route("/delete/<int:sno>")
def delete(sno):
    allObj = wadood.query.filter_by(sno=sno).first()
    db.session.delete(allObj)
    db.session.commit()
    print(allObj)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)