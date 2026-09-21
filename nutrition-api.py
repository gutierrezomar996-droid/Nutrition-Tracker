import os
import requests
from dotenv import load_dotenv

load_dotenv()
print(os.getenv('USDA_API_KEY'))

def search_food(food_name):
    api_key = os.getenv('USDA_API_KEY')

    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={api_key}"

    response  = requests.get(url)

    data = response.json()
    return data


def get_nutrition(food_name):
    # get raw data from USDA
    data = search_food(food_name)
    nutrients = data["foods"][0]["foodNutrients"]

    # make a translation table
    nutrient_map = {
        "Energy": "calories", 
        "Protein": "protein", 
        "Total lipid (fat)": "fat", 
        "Carbohydrate, by difference": "carbs", 
        "Sodium, Na": "sodium", 
        "Fiber, total dietary": "fiber", 
        "Total Sugars": "sugar", 
        "Calcium, Ca": "calcium", 
        "Iron, Fe": "iron", 
        "Vitamin A, IU": "vitamin_a",
        "Vitamin C, total ascorbic acid": "vitamin_c", 
        "Cholesterol": "cholesterol", 
        "Potassium, K": "potassium", 
        "Magnesium, Mg": "magnesium", 
        "Zinc, Zn": "zinc" 


    }

    # create empty dictionary and set keys to None
    nutrition = {key: None for key in nutrient_map.values()}

    #loop through every nutrient returned
    for nutrient in nutrients:
        name = nutrient["nutrientName"]
        
        # loop and select only nutrients you care abt
        if name in nutrient_map:
            key = nutrient_map[name]        # translate the name
            nutrition[key] = nutrient["value"]

    return {
        "food_name": data["foods"][0]["description"],
        **nutrition
    }



    #Set Macros to None incase api doesnt call return them. Same with micros
    calories = None
    protein = None
    fat = None
    carbs = None

    #set micros to None
    sodium = None
    fiber = None
    sugar = None
    cholesteral = None 
    potassium = None
    iron = None
    zinc = None
    magnesium = None
    calcium = None
    vitamin_a = None
    vitamin_b = None
    vitamin_c  = None
    vitamin_e = None
    vitamin_k = None


   

if __name__ == "__main__":
    result = get_nutrition("Chicken Breast")
    print(result)
