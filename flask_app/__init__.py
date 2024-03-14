from flask import Flask

app = Flask(__name__)

DATABASE = "readerscorner_db"

from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)


app.secret_key = "This is fun"