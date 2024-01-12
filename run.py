from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
#yorum satırı

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

# app.py