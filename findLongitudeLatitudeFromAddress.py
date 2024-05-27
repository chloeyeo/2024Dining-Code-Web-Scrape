from geopy.geocoders import Nominatim

# Initialize the geocoder
geolocator = Nominatim(user_agent="my_geocoder")

# Address to search
address = "제주특별자치도 제주시 첨단로 242"

# Perform the geocoding
location = geolocator.geocode(address)

# Check if the location was found successfully
if location:
    # Extract latitude and longitude
    latitude = location.latitude
    longitude = location.longitude
    print("Latitude:", latitude)
    print("Longitude:", longitude)
else:
    print("Location not found.")
