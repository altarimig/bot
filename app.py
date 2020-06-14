from flask import Flask
from src.routes.route import get_post



app = Flask(__name__)


get_post(app)

if __name__ == "__main__":
    app.run()
