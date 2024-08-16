from django.shortcuts import render
from hotel.models import Hotel, Booking, ActivityLog, StaffOnDuty, Room, RoomType, HotelGallery, HotelFeatures, HotelFaqs

def index(request):
    hotels = Hotel.objects.filter(status="Live")
    context = {
        "hotels":hotels
    }
    return render(request, "hotel/hotel.html",  context)

# Create your views here.

def hotel_detail(request, slug):
    hotel = Hotel.objects.get(status="Live", slug=slug)
    context = {
        "hotel":hotel,
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

    print("checkin ======", checkin)

    # if not all([checkin, checkout]):
    #     messages.warning(request, "Please enter your booking data to check availability.")
    #     return redirect("booking:booking_data", hotel.slug)

    context = {
        "hotel":hotel,
        "room_type":room_type,
        "rooms":rooms,
        "id":id,
        "checkin":checkin,
        "checkout":checkout,
        "adult":adult,
        "children":children,
        "room_type_":room_type_,
    }
    return render(request, "hotel/room_type_detail.html", context)

