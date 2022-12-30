from flask import Flask,render_template,current_app,appcontext_pushed,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
import os

picsFolder=os.path.join('static')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['UPLOAD_FOLDER']=picsFolder


db=SQLAlchemy(app)




app.app_context().push()

class Todo(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100))
    complete=db.Column(db.Boolean,default=False)

@app.route('/')
def index():
    pics1=os.path.join(app.config['UPLOAD_FOLDER'],'download.jpg')
    todo_list=Todo.query.all()
    total_todo=Todo.query.count()
    completed_todo=Todo.query.filter_by(complete=True).count()
    uncompleted_todo=total_todo-completed_todo
    return render_template('dashboard/index.html',**locals(),user_img=pics1)




@app.route('/add',methods=['POST'])
def add():
    title=request.form.get('title')
    new_todo=Todo(title=title,complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/update/<int:id>')
def update(id):
    todo=Todo.query.filter_by(id=id).first()
    todo.complete=not todo.complete
    db.session.commit()
    return redirect(url_for('index'))




@app.route('/about')
def about():
    return render_template('dashboard/about.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)