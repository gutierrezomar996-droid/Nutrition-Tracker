from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Meal
from nutrition_api import get_nutrition
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'nutrition-tracker-secret-key'

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



@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    if request.method == 'POST':
        calorie_goal = request.form.get('calorie_goal', 2000)  #2000 is the default cals. User can manually enter later.
        session['calorie_goal'] = int(calorie_goal)
        return redirect(url_for('history'))
    current_goal = session.get('calorie_goal', 2000)
    return render_template('settings.html', current_goal=current_goal)


#route for search
@app.route('/search', methods = ['POST'])
def search():
    food_name = request.form['food_name']

    grams_input = request.form.get('grams', '').strip()  ## handles if user leaves grams section blank
    grams = float(grams_input) if grams_input else 100.0
        
    nutrition = get_nutrition(food_name, grams)

    if nutrition is None:
        return render_template('index.html', error="Food not found. Try searching a different food method.")
    return render_template('results.html', nutrition=nutrition)




#route for food log
@app.route('/log', methods =['POST'])
def log_meal():
    meal = Meal(
        food_name = request.form['food_name'],
        serving_size = request.form.get('serving_size'),
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

    db.session.add(meal)
    db.session.commit()
    return redirect(url_for('history'))

#route for history
@app.route('/history')
def history():
    meals = Meal.query.order_by(Meal.date_logged.desc()).all()

    m = meals

    #meal calorie total
    totals = {
        'calories': round(sum(m.calories or 0 for m in meals),1),
        'protein': round(sum(m.protein or 0 for m in meals), 1),
        'fat': round(sum(m.fat or 0 for m in meals),1),
        'carbs': round(sum(m.carbs or 0 for m in meals),1)
    }

    calorie_goal = session.get('calorie_goal', 2000)
    remaining = round(calorie_goal - totals['calories'], 1)

    return render_template('history.html', meals = meals, totals=totals, calorie_goal=calorie_goal, remaining=remaining)



##App runner
@app.route('/delete/<int:meal_id>', methods = ['POST'])
def delete_meal(meal_id):
    meal = Meal.query.get_or_404(meal_id)
    db.session.delete(meal)
    db.session.commit()
    return redirect(url_for('history'))



if __name__ == '__main__':
    app.run(debug=True)