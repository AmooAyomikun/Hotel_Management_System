from django.shortcuts import render,redirect
from hotel.models import Hotel, Booking, ActivityLog, StaffOnDuty, Room, RoomType, HotelGallery, HotelFeatures, Notification, HotelFaqs, Coupon, Bookmark, Review
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone


from decimal import Decimal
from django.conf import settings
import stripe

from django.urls  import reverse


from datetime import datetime

from hotel.management.commands.update_coordinates import geocode_address
# def get_nearby_hotels_by_address(address, radius=5000):
#     lat, lon = geocode_address(address)
#     if lat and lon:
#         hotels = Hotel.objects.raw('''
#             SELECT * FROM yourapp_hotel
#             WHERE ST_DistanceSphere(POINT(longitude, latitude), POINT(%s, %s)) < %s
#         ''', [lon, lat, radius])
#         return hotels
#     return None

def index(request):
    hotels = Hotel.objects.filter(status="Live")
    context = {
        "hotels":hotels
    }
    return render(request, "hotel/hotel.html",  context)

# Create your views here.

def hotel_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)

    if request.user.is_authenticated:
        bookmark = Bookmark.objects.filter(user=request.user, hotel=hotel)
    else:
        bookmark = None

    all_reviews = Review.objects.filter(hotel=hotel)

    try:
        reviews = Review.objects.filter(user=request.user, hotel=hotel)
    except:
        reviews = None
    

    context = {
        "hotel":hotel,
        "bookmark":bookmark,
        "reviews":reviews,
        "all_reviews":all_reviews,
     }
    return render(request, "hotel/hotel_detail.html", context)


def room_type_detail(request, slug, rt_slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    room_type = RoomType.objects.get(hotel=hotel, slug=rt_slug)
    rooms = Room.objects.filter(room_type=room_type, is_available=True)

    id = request.GET.get("hotel-id")
    checkin = request.GET.get("checkin")
    checkout = request.GET.get("checkout")
    adult = request.GET.get("adult")
    children = request.GET.get("children")
    room_type_ = request.GET.get("room-type")

    print("ID ==========", id)

    if not all([checkin, checkout]):
        messages.warning(request, "Please enter your booking data to check availability.")
        return redirect("booking:booking_data", hotel.slug)

    context = {
         "hotel":hotel,
         "room_type":room_type,
         "rooms":rooms,
         "checkin":checkin,
         "checkout":checkout,
         "adult":adult,
         "children":children,
         "id":id,
         "room_type_":room_type_,
    }
    
    return render(request, "hotel/room_type_detail.html", context)

def selected_rooms(request):
    total = 0  
    room_count = 0
    total_days = 0
    adult = 0 
    children = 0 
    checkin = "" 
    checkout = "" 
    children = 0 
    
    if 'selection_data_obj' in request.session:
        if request.method == "POST":
            for h_id, item in request.session['selection_data_obj'].items():
                id = int(item['hotel_id'])
                # hotel_id = int(item['hotel_id'])
                checkin = item["checkin"]
                checkout = item["checkout"]
                adult = int(item["adult"])
                children = int(item["children"])
                room_type_ = item["room_type"]
                room_id = int(item["room_id"])
                
                user = request.user
                hotel = Hotel.objects.get(id=id)
                room = Room.objects.get(id=room_id)
                room_type = RoomType.objects.get(id=room_type_)

            date_format = "%Y-%m-%d"
            checkin_date = datetime.strptime(checkin, date_format)
            checout_date = datetime.strptime(checkout, date_format)
            time_difference = checout_date - checkin_date
            total_days = time_difference.days

            full_name = request.POST.get("full_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")

            booking = Booking.objects.create(
                hotel=hotel,
                room_type=room_type,
                check_in_date=checkin,
                check_out_date=checkout,
                total_days=total_days,
                num_adults=adult,
                num_children=children,
                full_name=full_name,
                email=email,
                phone=phone,
                user=request.user or None,
                payment_status = "Processing",
            )

            if request.user.is_authenticated:
                booking.user = request.user
                booking.save()
            else:
                booking.user = None
                booking.save()

            for h_id, item in request.session['selection_data_obj'].items():
                room_id = int(item["room_id"])
                room = Room.objects.get(id=room_id)
                booking.room.add(room)

                room_count += 1
                days = total_days
                price = room_type.price

                room_price = price * room_count
                total = room_price * days

            booking.total += float(total)
            booking.before_discount += float(total)
            booking.save()

            messages.success(request, "Checkout Now!")
            return redirect("hotel:checkout", booking.booking_id)

        hotel = None
        for h_id, item in request.session['selection_data_obj'].items():
            id = int(item['hotel_id'])
            hotel_id = int(item['hotel_id'])

            checkin = item["checkin"]
            checkout = item["checkout"]
            adult = int(item["adult"])
            children = int(item["children"])
            room_type_ = item["room_type"]
            room_id = int(item["room_id"])  

            # user = request.user
            # hotel = Hotel.objects.get(id=id)
            # room = Room.objects.get(id=room_id)
            room_type = RoomType.objects.get(id=room_type_)

            date_format = "%Y-%m-%d"
            checkin_date = datetime.strptime(checkin, date_format)
            checout_date = datetime.strptime(checkout, date_format)
            time_difference = checout_date - checkin_date
            total_days = time_difference.days 

            room_count += 1
            days = total_days
            price = room_type.price 

            room_price = price * room_count
            total = room_price * days

            hotel = Hotel.objects.get(id=id)
        
        context = {
            "data":request.session['selection_data_obj'], 
            "total_selected_items": len(request.session['selection_data_obj']),
            "total":total,
            "total_days":total_days,
            "adult":adult,
            "children":children,   
            "checkin":checkin,   
            "checkout":checkout,   
            "hotel":hotel,   
        }
        return render (request, "hotel/selected_rooms.html", context)

                   
    else:
        messages.warning(request, "No selected rooms yet")
        return redirect("/")

# def checkout(request, booking_id):
#     booking = Booking.objects.get(booking_id=booking_id)
#     if request.method == "POST":
#         code = request.POST.get("code")
#         try:
#             coupon = Coupon.objects.get(code__iexact=code, active=True)
#             if coupon in booking.coupons.all():
#                 messages.warning(request, "Coupon Already Activated")
#                 return redirect("hotel:checkout", booking.booking_id)
#             else:
#                 if coupon.type == "Percentage":
#                     discount = booking.total * coupon.discount / 100
#                 else:
#                     discount = coupon.discount

#                     booking.coupons.add(coupon)
#                     booking.total -= discount
#                     booking.saved += discount
#                     booking.save()

                
#                     messages.success(request, "Coupon Activated")
#                     return redirect("hotel:checkout", booking.booking_id)
#         except:
#             messages.error(request, "Coupon Does Not Exists")
#             return redirect("hotel:checkout", booking.booking_id)
#     context={
#         "booking":booking
#     }
#     return render(request, "hotel/checkout.html", context)
def checkout(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    if request.method == "POST":
        code = request.POST.get("code")
        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)
            if coupon in booking.coupons.all():
                messages.warning(request, "Coupon Already Activated")
                return redirect("hotel:checkout", booking.booking_id)
            else:
                if coupon.type == "Percentage":
                    discount = booking.total * coupon.discount / 100
                else:
                    discount = coupon.discount

                booking.coupons.add(coupon)
                booking.total -= discount
                booking.saved += discount
                booking.save()

                messages.success(request, "Coupon Activated")
                return redirect("hotel:checkout", booking.booking_id)
        except Coupon.DoesNotExist:
            messages.error(request, "Coupon Does Not Exist")
            return redirect("hotel:checkout", booking.booking_id)
    context = {
        "booking": booking,


    }
    return render(request, "hotel/checkout.html", context)

def payment_success(request, booking_id):
    success_id = request.GET.get('success_id')
    booking_total = request.GET.get('booking_total')

    if success_id and booking_total:
        success_id = success_id.rstrip("/")
        booking_total = booking_total.rstrip("/")

        booking = Booking.objects.get(booking_id = booking_id, success_id = success_id)

        if booking.total == Decimal(booking_total):
            print("Booking total matched")
            if booking.payment_status == "processing":
                booking.payment_status = "paid"
                booking.is_active = True
                booking.save()

                noti = Notification.objects.create(
                    booking=booking,
                    type = "Booking Confirmed"
                )
                if request.user.is_authenticated:
                    noti.user = request.user
                else:
                    noti.user = None

                noti.save()

                if 'selection_data_obj'  in request.session:
                    del request.session['selection_data_onj']

            else:
                messages.success(request, "Payment made already, thanks for your patronage")
                # return redirect("/")
        else:
            messages.error(request,"Error: Payment manipulation detected")

    context = {
        "booking":booking
    }
    return render (request, "hotel/payment_success.html", context)

def payment_failed(request, booking_id):
   return render (request, "hotel/payment_failed_html")

@csrf_exempt
def update_room_status(request):
    today = timezone.now().date()

    booking = Booking.objects.filter(is_active=True, payment_status="paid")   
    for b in booking:
        if b.checked_in_tracker != True:
            if b.check_in_date > today:
                b.checked_in_tracker = False
                b.checked_in = False
                b.save()

                for r in b.room.all():
                    r.is_available = True
                    r.save()
                

            else:
                b.checked_in_tracker = True
                b.checked_in = True
                b.save()

                for r in b.room.all():
                    r.is_available = False
                    r.save()
        else:
            if b.check_out_date > today:
                b.checked_out_tracker = False
                b.checked_in = False
                b.save()

                for r in b.room.all():
                    r.is_available = False
                    r.save()

            else:
                b.checked_out_tracker = True
                b.checked_in = True
                b.save()

                for r in b.room.all():
                    r.is_available = True
                    r.save()
    
    return HttpResponse(today)

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout_session(request, booking_id):
    # request_data = json.loads(request.body)
    # booking = Booking.objects.get(Booking, booking_id=booking_id)
    booking = Booking.objects.get(booking_id=booking_id)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email = booking.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': booking.full_name,
                    },
                    'unit_amount': int(booking.total * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('hotel:success', args=[booking.booking_id])) + "?session_id={CHECKOUT_SESSION_ID}&success_id="+booking.success_id+'&booking_total='+str(booking.total),
        cancel_url=request.build_absolute_uri(reverse('hotel:failed', args=[booking.booking_id]))+ "?session_id={CHECKOUT_SESSION_ID}",
    )

    booking.payment_status = "processing"
    booking.stripe_payment_intent = checkout_session['id']
    booking.save()

    print("checkout_session ==============", checkout_session)
    return JsonResponse({'sessionId': checkout_session.id})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from userauths.forms import HotelForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


@login_required
def hotelier_add_hotel(request):
    """
    View to handle the creation of a new hotel by a hotel owner.
    Only accessible to authenticated users.
    """
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.user = request.user  # Assign the logged-in user as the hotel owner
            hotel.save()
            form.save_m2m()  
            messages.success(request, 'Hotel added successfully!')
            return redirect('index')  # Replace with your actual redirect target
        else:
            messages.error(request, 'Error adding hotel. Please check the form.')
    else:
        form = HotelForm()
    return render(request, 'hotel/hotelier_add_hotel.html', {'form': form})


# from hotel.management.commands.update_coordinates import geocode_address
# def get_nearby_hotels_by_address(address, radius=5000):
#     lat, lon = geocode_address(address)
#     if lat and lon:
#         hotels = Hotel.objects.raw('''
#             SELECT * FROM hotel_hotel
#             WHERE ST_DistanceSphere(
#                 ST_MakePoint(longitude, latitude)::geography,
#                 ST_MakePoint(%s, %s)::geography
#             ) < %s
#         ''', [lon, lat, radius])
#         return hotels
#     return None

# def get_nearby_hotels_by_address(address, radius=5000):
#     lat, lon = geocode_address(address)
#     if lat and lon:
#         hotels = Hotel.objects.raw('''
#             SELECT *, (
#                 6371000 * acos(
#                     cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude) - radians(%s)) +
#                     sin(radians(%s)) * sin(radians(latitude))
#                 )
#             ) AS distance
#             FROM hotel_hotel
#             WHERE (
#                 6371000 * acos(
#                     cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude) - radians(%s)) +
#                     sin(radians(%s)) * sin(radians(latitude))
#                 )
#             ) < %s
#             ORDER BY distance
#         ''', [lat, lon, lat, lat, lon, lat, radius])
#         return hotels
#     return None


# def search_hotels_view(request):
#     address = request.GET.get('address')
#     hotels = None
#     if address:
#         hotels = get_nearby_hotels_by_address(address)
#     else:
#         messages.info(request, 'Please enter an address to search for hotels.')
    
#     return render(request, "hotel/hotel.html",  {'hotels': hotels})

# def search_hotels_view(request):
#     address = request.GET.get('address')  # Address input from user
#     hotels = None  # Initialize hotels as None

#     if address:
#         hotels = get_nearby_hotels_by_address(address)
    
#     context = {
#         'hotels': hotels,
#     }
#     return render(request, "hotel/hotel.html", {'hotels': hotels, 'address': address})
# def search_hotels_view(request):
#     address = request.GET.get('address')  # Address input from user

#     # Initialize hotels as None, so no hotels are shown initially
#     hotels = None

#     if address:  # Only search when the address is provided
#         hotels = get_nearby_hotels_by_address(address)

#     context = {
#         'hotels': hotels,  # This will be None if no address is searched
#         'address': address,
#     }
#     return render(request, "hotel/hotel.html", context)


# def search_hotels_view(request):
#     address = request.GET.get('address')  # Address input from user
#     hotels = []  # Initialize hotels as an empty list

#     if address:  # Only search when the address is provided
#         hotels = get_nearby_hotels_by_address(address) or []  # Ensure hotels is an empty list if nothing is found

#     context = {
#         'hotels': hotels,  # This will be an empty list if no address is searched or no hotels found
#         'address': address,
#     }
#     return render(request, "hotel/hotel.html", context)

# views.py
# from django.shortcuts import render
# from .models import Hotel

# def search_hotels_view(request):
#     address = request.GET.get('address', '')  # Get the entered address
#     if address:
#         hotels = Hotel.objects.filter(address__icontains=address)  # Case-insensitive partial match
#     else:
#         hotels = Hotel.objects.all()  # Default to all hotels if no address is entered

#     context = {
#         'hotels': hotels,  # This will be an empty list if no address is searched or no hotels found
#         'address': address,
#     }
#     return render(request, "hotel/hotel.html", context)
    
import requests
from django.conf import settings
# from hotel.settings  import GEOAPIFY_API_KEY 
from django.shortcuts import render
from hotel.models import Hotel
geoapify_key = settings.GEOAPIFY_API_KEY
# geoapify_url = f"https://api.geoapify.com/v2/places?categories=accommodation.hotel&text={address}&apiKey={b6c977ce7ff54985a263958fcb4ca782}"



# def search_hotels_view(request):
#     address = request.GET.get('address', '')  # Get the entered address
#     hotels = []

#     if address:
#         # First, check for hotels in the database
#         hotels = Hotel.objects.filter(address__icontains=address)
        
#         # If no hotels found in the database, call Geoapify API
#         if not hotels:
#             geoapify_key = settings.GEOAPIFY_API_KEY
#             geoapify_url = f"https://api.geoapify.com/v2/places?categories=accommodation.hotel&text={address}&apiKey={geoapify_key}"
#             print("Geoapify Request URL:", geoapify_url)
#             response = requests.get(geoapify_url)
#             response = requests.get(geoapify_url)
#             print("Geoapify Response Status Code:", response.status_code)
#             data = response.json()
#             print("Geoapify Response Data:", data)
#             data = response.json()

#             # Process Geoapify API response
#             hotels = []
#             if 'features' in data:
#                 for feature in data['features']:
#                     properties = feature['properties']
#                     hotel_info = {
#                         'name': properties.get('name', 'Unknown'),
#                         'address': properties.get('formatted', 'No address'),
#                         'rating': properties.get('rating', 'No rating'),
#                         'reviews': properties.get('reviews', 'No reviews'),
#                         'image': properties.get('icon', 'No image')
#                     }
#                     hotels.append(hotel_info)

#     context = {
#         'hotels': hotels,  # This will be an empty list if no address is searched or no hotels found
#         'address': address,
#     }
#     return render(request, "hotel/hotel.html", context)

import requests
from django.conf import settings
from django.shortcuts import render
from .models import Hotel
from hotel.management.commands.update_coordinates import geocode_address

# def search_hotels_view(request):
#     address = request.GET.get('address', '')  # Get the entered address
#     hotels = Hotel.objects.filter(address__icontains=address) if address else Hotel.objects.all()
    
#     # If no hotels found in the database, search via Geoapify API
#     if address and not hotels.exists():
#         lat, lon = geocode_address(address)  # Get latitude and longitude of the address
        
#         if lat and lon:
#             # Construct Geoapify API URL for nearby hotels
#             geoapify_url = (
#                 f"https://api.geoapify.com/v2/places?categories=accommodation.hotel&filter=circle:{lon},{lat},5000"
#                 f"&limit=10&apiKey={settings.GEOAPIFY_API_KEY}"
#             )
#             response = requests.get(geoapify_url)
            
#             # Check if the API call was successful
#             if response.status_code == 200:
#                 geoapify_data = response.json()
#                 hotels = []
                
#                 # Parse the Geoapify response and format hotels
#                 for feature in geoapify_data.get('features', []):
#                     properties = feature.get('properties', {})
#                     hotel = {
#                         'name': properties.get('name'),
#                         'address': properties.get('formatted'),
#                         'reviews': properties.get('reviews', 'N/A'),  # Add reviews if available
#                         'rating': properties.get('rating', 'N/A'),    # Add rating if available
#                         'distance': feature.get('distance', 0),       # Distance from the searched address
#                         'image': None  # Geoapify may not return an image; set as None or a placeholder
#                     }
#                     hotels.append(hotel)
#             else:
#                 hotels = []  # Handle case if API fails to return data
#         else:
#             hotels = []  # No latitude/longitude available for the searched address
    
#     context = {
#         'hotels': hotels,
#         'address': address,
#     }
#     return render(request, "hotel/hotel.html", context)
import requests
from django.conf import settings
from django.shortcuts import render
from .models import Hotel
# from hotel.management.commands.update_coordinates import geocode_address
from geopy.distance import geodesic  

def search_hotels_view(request):
    address = request.GET.get('address', '')  # Get the entered address
    hotels = Hotel.objects.filter(address__icontains=address) if address else Hotel.objects.all()
    
    if not hotels.exists() and address:
        lat, lon = geocode_address(address)  # Get latitude and longitude of the address
        
        if lat and lon:
            # Find the nearest hotel in the database to the searched address
            nearest_hotel = find_nearest_hotel(lat, lon)
            if nearest_hotel:
                hotels = [{
                    'name': nearest_hotel.name,
                    'address': nearest_hotel.address,
                    'reviews': 'N/A',
                    'rating': 'N/A',
                    'distance': calculate_distance(lat, lon, nearest_hotel.latitude, nearest_hotel.longitude),
                    'image': None
                }]
            else:
                hotels = []  # No hotels found in the database
        else:
            hotels = []  # No latitude/longitude available for the searched address
    else:
        # Convert queryset to list of dictionaries for rendering
        hotels = [{
            'name': hotel.name,
            'address': hotel.address,
            'reviews': 'N/A',
            'rating': 'N/A',
            'distance': 0,
            'image': None
        } for hotel in hotels]
    
    context = {
        'hotels': hotels,
        'address': address,
    }
    return render(request, "hotel/hotel.html", context)

def find_nearest_hotel(lat, lon):
    nearest_hotel = None
    min_distance = float('inf')
    for hotel in Hotel.objects.all():
        distance = calculate_distance(lat, lon, hotel.latitude, hotel.longitude)
        if distance < min_distance:
            min_distance = distance
            nearest_hotel = hotel
    return nearest_hotel

def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).meters

# def search_hotels_view(request):
#     address = request.GET.get('address', '')  # Get the entered address
#     hotels = Hotel.objects.filter(address__icontains=address) if address else Hotel.objects.all()
    
#     if not hotels.exists() and address:
#         lat, lon = geocode_address(address)  # Get latitude and longitude of the address
        
#         if lat and lon:
#             # Construct Geoapify API URL for nearby hotels
#             geoapify_url = (
#                 f"https://api.geoapify.com/v2/places?categories=accommodation.hotel&filter=circle:{lon},{lat},5000"
#                 f"&limit=10&apiKey={settings.GEOAPIFY_API_KEY}"
#             )
#             response = requests.get(geoapify_url)
            
#             if response.status_code == 200:
#                 geoapify_data = response.json()
#                 geoapify_hotels = []
                
#                 # Parse the Geoapify response and format hotels
#                 for feature in geoapify_data.get('features', []):
#                     properties = feature.get('properties', {})
#                     hotel = {
#                         'name': properties.get('name'),
#                         'address': properties.get('formatted'),
#                         'reviews': properties.get('reviews', 'N/A'),
#                         'rating': properties.get('rating', 'N/A'),
#                         'distance': feature.get('distance', 0),
#                         'image': None
#                     }
#                     geoapify_hotels.append(hotel)
                
#                 # Find the nearest hotel in the database
#                 nearest_hotel = find_nearest_hotel(lat, lon)
#                 if nearest_hotel:
#                     # Add the nearest hotel to the results
#                     nearest_hotel_info = {
#                         'name': nearest_hotel.name,
#                         'address': nearest_hotel.address,
#                         'reviews': 'N/A',
#                         'rating': 'N/A',
#                         'distance': calculate_distance(lat, lon, nearest_hotel.latitude, nearest_hotel.longitude),
#                         'image': None
#                     }
#                     geoapify_hotels.append(nearest_hotel_info)
#             else:
#                 geoapify_hotels = []  # Handle case if API fails to return data
#         else:
#             geoapify_hotels = []  # No latitude/longitude available for the searched address
#         hotels = geoapify_hotels
    
#     context = {
#         'hotels': hotels,
#         'address': address,
#     }
#     return render(request, "hotel/hotel.html", context)

# def find_nearest_hotel(lat, lon):
#     # Implement the logic to find the nearest hotel in the database
#     nearest_hotel = None
#     min_distance = float('inf')
#     for hotel in Hotel.objects.all():
#         distance = calculate_distance(lat, lon, hotel.latitude, hotel.longitude)
#         if distance < min_distance:
#             min_distance = distance
#             nearest_hotel = hotel
#     return nearest_hotel

# def calculate_distance(lat1, lon1, lat2, lon2):
#     # Implement the Haversine formula or use a library to calculate the distance
#     from geopy.distance import geodesic
#     return geodesic((lat1, lon1), (lat2, lon2)).meters
