import requests
import json
from geopy.geocoders import Nominatim
import random

# Function to select random foodType and mateType
def select_types():
    food_types = ["한식", "양식", "중식", "일식", "디저트"]
    mate_types = ["연인", "친구", "가족", "단체모임", "반려동물", "혼밥"]
    food_type = random.choice(food_types)
    mate_type = random.sample(mate_types, k=random.randint(1, 3))
    return food_type, mate_type

print(select_types())