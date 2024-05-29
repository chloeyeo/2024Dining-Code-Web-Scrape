import json
import time
'''
Nominatim is a geocoding service provided by OpenStreetMap
(OSM). It's a tool used for converting addresses into
geographic coordinates (latitude and longitude).
'''
from geopy.geocoders import Nominatim
import random

# Function to get coordinates from address using Nominatim
def get_coordinates(address):
    geolocator = Nominatim(user_agent="restaurant_coordinate_locator")
    max_retries = 3
    retries = 0
    
    while retries < max_retries:
        try:
            location = geolocator.geocode(address, timeout=10)  # Increase timeout if needed
            if location:
                return [location.longitude, location.latitude]
            else:
                return []
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
            retries += 1
            time.sleep(1)  # Add a delay before retrying
    
    print("Exceeded maximum retries. Unable to get coordinates.")
    return []
    
# addr = "서울특별시 강남구 논현동 116-3"
# print(get_coordinates(addr))

# Function to select random foodType and mateType
def select_types():
    food_types = ["한식", "양식", "중식", "일식", "디저트"]
    mate_types = ["연인", "친구", "가족", "단체모임", "반려동물", "혼밥"]
    food_type = random.choice(food_types)
    mate_type = random.sample(mate_types, k=random.randint(1, 3))
    return food_type, mate_type

# Load data from file
with open('all_restaurants2.json', 'r', encoding='utf-8') as file:
    restaurants = json.load(file)

for restaurant in restaurants:
    address = f"{restaurant['address']['metropolitan']} {restaurant['address']['city']} {restaurant['address']['district']} {restaurant['address']['detailedAddress']}"
    
    # Get coordinates from address
    coordinates = get_coordinates(address)
    restaurant['location']["coordinates"] = coordinates
    
    # Select random foodType and mateType
    food_type, mate_type = select_types()
    restaurant['category'] = [{"foodType": food_type}, {"mateType": mate_type}]



# save updated data in correct format to put in db
with open('all_restaurants_correct_format.txt', 'w', encoding='utf-8') as file:
    json.dump(restaurants, file, indent=4)