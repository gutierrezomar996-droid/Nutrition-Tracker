import os
import requests
from dotenv import load_dotenv

load_dotenv()


def search_food(food_name):
    api_key = os.getenv('USDA_API_KEY')

    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_name}&api_key={api_key}"

    response  = requests.get(url)

    data = response.json()
    return data



def find_best_match(foods,food_name):
    food_name_lower = food_name.lower()


    for food in foods:
        description = food["description"].lower()
        if food_name_lower in description and "raw" in description:
            return food

    for food in foods:
        description = food["description"].lower()
        if food_name_lower == description:
            return food

    return foods[0]




def get_nutrition(food_name, grams=100):

    # get raw data from USDA
    data = search_food(food_name)
    best_match = find_best_match(data["foods"], food_name)
    nutrients = best_match["foodNutrients"]
    multiplier = grams / 100 # --> grams multiplier

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
            
    # if the database cant access the nutrition it will save and return 0
    return {
    "food_name": best_match["description"],
    "serving_size": grams,
    "calories": round((nutrition["calories"] or 0) * multiplier, 2), # 2 = round to 2 decimals
    "protein": round((nutrition["protein"] or 0) * multiplier, 2),
    "fat": round((nutrition["fat"] or 0) * multiplier, 2),
    "carbs": round((nutrition["carbs"] or 0) * multiplier, 2),
    "sodium": round((nutrition["sodium"] or 0) * multiplier, 2),
    "fiber": round((nutrition["fiber"] or 0) * multiplier, 2),
    "sugar": round((nutrition["sugar"] or 0) * multiplier, 2),
    "calcium": round((nutrition["calcium"] or 0) * multiplier, 2),
    "iron": round((nutrition["iron"] or 0) *multiplier, 2),
    "vitamin_a": round((nutrition["vitamin_a"] or 0) * multiplier, 2),
    "vitamin_c": round((nutrition["vitamin_c"] or 0) * multiplier, 2),
    "cholesterol": round((nutrition["cholesterol"] or 0) * multiplier, 2),
    "potassium": round((nutrition["potassium"] or 0) * multiplier, 2),
    "magnesium": round((nutrition["magnesium"] or 0) * multiplier, 2),
    "zinc": round((nutrition["zinc"] or 0) * multiplier, 2),
}


   

if __name__ == "__main__":
    result = get_nutrition("Chicken Breast")
    print(result)
