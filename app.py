from flask import Flask, render_template, request, redirect, url_for
from models import db, Meal
from nutrition_api import get_nutrition
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

##Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nutrition.db'     ##Where to store data
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Turn off unnecessary features

#Connect database to app
db.init_app(app)    

#create the tables from models
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


#route for search
@app.route('/search', methods = ['POST'])
def search():
    food_name = request.form['food_name']
    nutritoin = get_nutrition(food_name)
    return render_template('results.html', nutrition=nutrition)

#route for food log
@app.route('/log', methods =['POST'])
def lod_meal():
    meal = Meal(
        food_name = request.form['food_name'],
        calories = request.form.get('calories', 0),
        protein = request.form.get('protein', 0),
        fat = request.form.get('fat', 0),
        carbs = request.form.get('carbs'),
        sodium = request.form.get('sodium'),
        fiber = request.form.get('fiber'),
        sugar = request.form.get('sugar'),
        calcium = request.form.get('calcium'),
        iron = request.form.get('iron'),
        vitamin_a = request.form.get('vitamin_a'),
        vitamin_c = request.form.get('vitamin_c'),
        cholesterol = request.form.get('cholesterol'),
        potassium = request.form.get('potassium'),
        magnesium = request.form.get('magnesium'),
        zinc = request.form.get('zinc'),
        meal_type = request.form.get('meal_type')
    )

    db.session(meal)
    db.session.commit()
    return redirect(url_for('history'))

#route for history
@app.route('/history')
def history():
    meals = Meal.query.order_by(Meal.date_logged.desc()).all()
    return render_template('history.html', meals = meals)

##App runner
@app.route('/delete/<int:meal_id>', methods = ['POST'])
def delete_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)