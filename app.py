from todo_list_routes import todo_bp
from flask import Flask

app = Flask(__name__)
app.register_blueprint(todo_bp) # all routes for todo (blueprint) are registred in app

if __name__ == "__main__":
    app.run(debug=True)