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




def get_nutrition(food_name):
    # get raw data from USDA
    data = search_food(food_name)

    best_match = find_best_match(data["foods"], food_name)
    nutrients = best_match["foodNutrients"]

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
    "calories": nutrition["calories"] or 0,
    "protein": nutrition["protein"] or 0,
    "fat": nutrition["fat"] or 0,
    "carbs": nutrition["carbs"] or 0,
    "sodium": nutrition["sodium"] or 0,
    "fiber": nutrition["fiber"] or 0,
    "sugar": nutrition["sugar"] or 0,
    "calcium": nutrition["calcium"] or 0,
    "iron": nutrition["iron"] or 0,
    "vitamin_a": nutrition["vitamin_a"] or 0,
    "vitamin_c": nutrition["vitamin_c"] or 0,
    "cholesterol": nutrition["cholesterol"] or 0,
    "potassium": nutrition["potassium"] or 0,
    "magnesium": nutrition["magnesium"] or 0,
    "zinc": nutrition["zinc"] or 0
}


   

if __name__ == "__main__":
    result = get_nutrition("Chicken Breast")
    print(result)
