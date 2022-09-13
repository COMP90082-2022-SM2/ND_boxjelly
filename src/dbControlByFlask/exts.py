# define db here, so multiple apps can import the same db object

from flask import Flask, request, redirect, render_template
# import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from config import MysqlConfig, sqliteConfig
# import flask_cors

app = Flask(__name__)
#CORS(app)

app.secret_key = "abc"
app.config.from_object(MysqlConfig)
app.permanent_session_lifetime = timedelta(minutes=1)
db = SQLAlchemy(app)