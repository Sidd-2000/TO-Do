from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.srno} - {self.title}"

# Create tables if they don't exist
with app.app_context():
    db.create_all()


@app.route("/",methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        todo = Todo(title=title, description=description)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html",allTodo=allTodo)


@app.route("/show")
def show():
    todo = Todo.query.all()
    print(todo)
    return "This is show page"



@app.route("/delete/<int:srno>")
def delete(srno):
    todo = Todo.query.filter_by(srno=srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")



@app.route("/update/<int:srno>",methods=["POST", "GET"])
def update(srno):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        todo = Todo.query.filter_by(srno=srno).first()
        todo.title = title
        todo.description = description
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(srno=srno).first()
    return render_template("update.html",todo = todo)



if __name__ == "__main__":
    app.run(debug=True, port=8000)
