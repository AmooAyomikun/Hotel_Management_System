from django.core.management.base import BaseCommand
from hotel.models import Hotel
import requests


GEOAPIFY_API_KEY = 'b6c977ce7ff54985a263958fcb4ca782'

def geocode_address(address):
    url = f'https://api.geoapify.com/v1/geocode/search?text={address}&apiKey={GEOAPIFY_API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if len(data['features']) > 0:
        coordinates = data['features'][0]['geometry']['coordinates']
        return coordinates[1], coordinates[0]  # returns latitude, longitude
    return None, None

def update_hotel_coordinates():
    hotels = Hotel.objects.filter(latitude__isnull=True, longitude__isnull=True)
    for hotel in hotels:
        lat, lon = geocode_address(hotel.address)
        if lat and lon:
            hotel.latitude = lat
            hotel.longitude = lon
            hotel.save()
            print(f"Updated {hotel.name} with coordinates: {lat}, {lon}")
        else:
            print(f"Could not find coordinates for {hotel.name}")

class Command(BaseCommand):
    help = 'Updates hotels with missing latitude and longitude based on their address'

    def handle(self, *args, **kwargs):
        update_hotel_coordinates()