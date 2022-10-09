from main import app
from exts import db
# from app.exts import db, app
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)