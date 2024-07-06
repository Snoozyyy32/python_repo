
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)
app.app_context().push()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    
@app.route('/', methods=['POST','Get'])
def index():
    if request.method == 'POST':
        #Create a vareable for the content column in the Todo class.
        task_content = request.form['content']
        #Create an object for the Todo class and set its conte nt table to the tesk_content variabl.
        new_task = Todo(content=task_content)
        #Add and save data into the database.
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem when adding your task."
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
#This code says make a variable wich displays all the entries in the Todo database based on date. 
    return render_template("index.html", tasks=tasks)
# Now we have passed the variable into our template (task=task).


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task."

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method =='POST':
#Now we set the the content of the task var we made to that of the for we are trying to update.
        task.content = request.form['content']
#Now we just commit the update.Note that we dont add new content we are just modifying old content.
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was trouble updating this task."
    else:
        return render_template('update.html', task=task)


    def __repr__(self) -> str:
        return '<Task %r>' % self.id





if __name__ == "__main__":
    app.run(debug=True)

