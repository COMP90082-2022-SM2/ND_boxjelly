from flask import Flask
from config import DevelopmentConfig
from exts import db
from flask_migrate import Migrate
from model import Case, Patient


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)

migrate = Migrate(app, db)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/get/<int:case_id>')
def query(case_id):  # put application's code here
    result = Case.query.filter_by(id=case_id).one()
    try:
        result = Case.query.filter_by(id=case_id).one()
        return repr(result)
    except:
        return 'record not found'

@app.route('/process', methods=['POST'])
def process_pdf():
    flag = True # check if the document is uploaded properly etc....
    return flag


if __name__ == '__main__':
    app.run()
