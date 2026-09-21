from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)


    #micro-nutrients, api wont call all
    sodium = db.Column(db.Float)
    fiber = db.Column(db.Float)
    sugar = db.Column(db.Float)
    cholesteral = db.Column(db.Float)
    potassium = db.Column(db.Float)
    iron = db.Column(db.Float)
    zinc = db.Column(db.Float)
    magnesium = db.Column(db.Float)
    calcium = db.Column(db.Float)
    vitamin_a = db.Column(db.Float)
    vitamin_b = db.Column(db.Float)
    vitamin_c  = db.Column(db.Float)
    vitamin_e = db.Column(db.Float)
    vitamin_k = db.Column(db.Float)

    #output. Dataset
    serving_size = db.Column(db.String(50))
    meal_type = db.Column(db.String(20))
    date_logged = db.Column(db.DateTime, default=datetime.utcnow)
                          


    def __repr__(self):
        return f'<Meal {self.food_name}>'
    