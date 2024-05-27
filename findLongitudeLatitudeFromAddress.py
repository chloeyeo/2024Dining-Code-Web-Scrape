from geopy.geocoders import Nominatim

# Initialize the geocoder
geolocator = Nominatim(user_agent="my_geocoder")

# Address to search
# need to get address of ALL 3200 restaurants
# then get its longitude and latitude using geopy
# then store the longitude and latitude as dataframe
# then combine with existing dataframe using df.concat
# (to combine the different columns for same rows)
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

# after this must finally work on putting categories
