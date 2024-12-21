from flask import Flask
from backend.routes.task_routes import task_routes
from backend.db.database import init_db

app = Flask(__name__)

# Initialize database
init_db()

# Register routes
app.register_blueprint(task_routes, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
