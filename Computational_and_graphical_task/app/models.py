from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    periodicity = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    next_due_date = db.Column(db.DateTime, nullable=False)
