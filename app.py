from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy

# create the app 
app = Flask(__name__)
app.debug = True

# create the extension
db = SQLAlchemy()

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# initialize the app with the extension
db.init_app(app)


#create the model
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String())
    done = db.Column(db.Boolean)

with app.app_context():
    db.create_all()




#home route
@app.route("/")
def home():
    return "Home Page"



# get all todo list
@app.route("/todo/list")
def getAllTodo():
    todoList = ToDo.query.all()
    result = {}
    for i in todoList:
        temp = {
            "Id" : i.id,
            "Name" : i.name,
            "Status" : i.done
        }
        result[i.id] = temp
    if(result == {}):
        return "There is no task on your list"
    return jsonify(result) 


#create a todo task 
@app.route('/todo/add', methods=['POST'])
def createTask():
    taskName = request.get_json().get("name")
    taskDescription = ""
    if(request.get_json().get("description") != None):
        taskDescription = request.get_json().get("description")
    newTask = ToDo(name = taskName,description = taskDescription, done = False)
    db.session.add(newTask)
    db.session.commit()
    return "Task add successfully..."


# to get a particular task
@app.route("/todo/<int:todoId>")
def getOneTask(todoId):
    todo = None
    todo = ToDo.query.get(todoId)
    if(todo == None):
        return "There is no task exist with this Id"
    result = {
        "id" : todo.id,
        "name" : todo.name,
        "description" : todo.description,
        "status" : todo.done
    }
    return jsonify(result)

#update a todo task 
#mark as complete or incomplete
@app.route("/todo/update/<int:todoId>", methods=['PATCH'])
def update(todoId):
    todo = None
    todo = ToDo.query.get(todoId)
    if(todo == None):
        return "There is no task exist with this Id"
    todo.done = not todo.done
    db.session.commit()
    return "Update successfully"


#delete a todo task 
@app.route("/todo/delete/<int:todoId>", methods = ['DELETE'])
def deleteTask(todoId):
    todo = None
    todo = ToDo.query.get(todoId)
    if(todo == None):
        return "There is no task exist with this Id"
    db.session.delete(todo)
    db.session.commit()
    return "deletion done"



if __name__ == "__main__":
    app.run(port=5000)


