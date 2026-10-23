import os
import requests
from dotenv import load_dotenv

load_dotenv()

def search_food(food_name):
    #search URL
    url = f"https://world.openfoodfacts.org/cgi/search.pl?search_terms={food_name}&json=true&page_size=10"

    #Identify app to open food facts
    headers =  {'User-Agent': 'Nutrition-Tracker/1.0'} 
    response  = requests.get(url, headers=headers)

    # handle empty or invalid responses
    if response.status_code != 200 or not response.text:
        return {"products": []}

    try:
        data = response.json()
        return data
    except Exception:
        return {"products: []"}

#find the closest matching product to the search
def find_best_match(products,food_name):
    food_name_lower = food_name.lower()
    #loop to find closest matching name
    for product in products:
       name = product.get("product_name", "").lower()   #if product has no name, returns empty string
       if food_name_lower in name or name in food_name_lower:
        return product
    # if else to fallback to the first result
    if products:
        return products[0]
    else:
        None


def get_nutrition(food_name, grams=100):
    data = search_food(food_name)
    #returns empty list if none are found
    products = data.get("products", [])     
    if not products:            #exits early if no data is found
        return None
    #returns empty list i
    best_match = find_best_match(products, food_name)
    if not best_match:      #--> exits early if no data is found
        return None
    
    #reaches to this point if data is found and gets returned.
    nutrition = best_match.get("nutriments", {}) # --> nutriments is the key word for finding nutrients from api request

    multiplier = grams / 100 # --> grams multiplier
            
    # if the database cant access the nutrition it will save and return 0
    return {
    "food_name": best_match.get("product_name", food_name),  # --> food_name parameter returns original searched name if api doesnt return one.
    "serving_size": grams,
    "calories": round((nutrition.get("energy-kcal_100g") or 0) * multiplier, 2), # 2 = round to 2 decimals
    "protein": round((nutrition.get("protiens_100g") or 0) * multiplier, 2),
    "fat": round((nutrition.get("fat_100g") or 0) * multiplier, 2),
    "carbs": round((nutrition.get("carbohydrates_100g") or 0) * multiplier, 2),
    "sodium": round((nutrition.get("sodium_100g") or 0) * multiplier, 2),
    "fiber": round((nutrition.get("fiber_100g") or 0) * multiplier, 2),
    "sugar": round((nutrition.get("sugars_100g")or 0) * multiplier, 2),
    "calcium": round((nutrition.get("calcium_100g") or 0) * multiplier, 2),
    "iron": round((nutrition.get("iron_100g") or 0) *multiplier, 2),
    "vitamin_a": round((nutrition.get("vitamin-a_100g") or 0) * multiplier, 2),
    "vitamin_c": round((nutrition.get("vitamin-c_100g") or 0) * multiplier, 2),
    "cholesterol": round((nutrition.get("cholesterol_100g") or 0) * multiplier, 2),
    "potassium": round((nutrition.get("potassium_100g") or 0) * multiplier, 2),
    "magnesium": round((nutrition.get("magnesium_100g") or 0) * multiplier, 2),
    "zinc": round((nutrition.get("zinc_100g")or 0) * multiplier, 2),
}


   

if __name__ == "__main__":
    result = get_nutrition("Chicken Breast")
    print(result)
