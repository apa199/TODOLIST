from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATION']=False

db=SQLAlchemy(app)


class TODODB(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    descp=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime(200),default=datetime.utcnow)

    def __repr__(self) ->str:
        return f"{self.sno} - {self.title}-{self.descp}"


@app.route("/",methods=["GET","POST"])
def main():
    if request.method=="POST":
        title=request.form['title']
        descp=request.form['descp']
        todo=TODODB(title=title, descp=descp)
        db.session.add(todo)
        db.session.commit()
    alltodo=TODODB.query.all()
    return render_template('index.html',alltodo=alltodo)


@app.route("/show")
def products():
   alltodo=TODODB.query.all()
   print(alltodo)
   return 'this is product page'

@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        title=request.form['title']
        descp=request.form['descp']
        todo=TODODB.query.filter_by(sno=sno).first()
        todo.title=title
        todo.descp=descp
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=TODODB.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=TODODB.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


   


if __name__ == "__main__":
    app.run(debug=True)