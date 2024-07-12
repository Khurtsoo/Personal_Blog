from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

app.config["SECRET_KEY"] = "lN2%jF1(eH2;bD4%bB2*cC4"
UPLOAD_FOLDER = 'C:\\Users\\LASHA\\Desktop\\blog\\static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
db = SQLAlchemy(app)

login_manager = LoginManager(app)