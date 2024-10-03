from flask import Flask, render_template, request, redirect
from scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create my app
app = Flask(__name__)
# Scss(app)


# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class MyTask(db.Model):
    __tablename__ = "Task Attributes"
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, default=0)
    created = db.Column(db.DateTime, default = datetime.now())
    
    def __repr__(self) -> str:
        return f"Task {self.id}"

with app.app_context():
        db.create_all()
 
# Route for webpages
# Home page        
@app.route("/", methods = ["GET","POST"])
def index():
    # Add task
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = MyTask(content=current_task)
        
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
            
        except Exception as e:
            print(f"ERROR: {e}")            
            return (f"ERROR: {e}")            
    
    else: 
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks = tasks)
    
# Delete Item from Task List
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    
    try: 
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
        
    except Exception as e:
        print(f"ERROR: {e}")            
        return (f"ERROR: {e}")   

# Edit item from task list
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    """
    Edit item from task list
    
    Args:
        id (int): ID of the task to be edited
    
    Returns:
        str: HTML code for the edit page
    """
    
    edit_item = MyTask.query.get_or_404(id)
    
    if request.method == "POST":
        edit_item.content = request.form["content"]
        edit_item.complete = True if request.form.get("complete") else False
        
        try: 
            db.session.commit()
            return redirect("/")
        
        except Exception as e:
            print(f"ERROR: {e}")            
            return (f"ERROR: {e}") 
        
    else:
        return render_template("edit.html", task = edit_item)
        
if __name__ == "__main__":
    
    
    app.run(debug=True)

