from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from hotel.models import Hotel,Booking, ActivityLog, StaffOnDuty, Room, RoomType, HotelGallery, HotelFeatures, HotelFaqs

def check_room_availability(request):
    if request.method == "POST":
        id = request.POST.get("hotel-id")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        adult = request.POST.get("adult")
        children = request.POST.get("children")
        room_type = request.POST.get("room-type")

        hotel = Hotel.objects.get(status="Live", id=id)
        room_type = RoomType.objects.get(hotel=hotel, slug=room_type)
        
        print("id ====", id)
        print("room_type ====", room_type)
        print("checkin ====", checkin)
        print("checkout ====", checkout)
        print("adult ====", adult)
        print("children ====", children)
        print("hotel ====", hotel)
        


        # return redirect("hotel:room_type_detail", hotel.slug, room_type.slug)
        url = reverse("hotel:room_type_detail", args=[hotel.slug, room_type.slug])
        url_with_params = f"{url}?hotel-id={id}&checkin={checkin}&checkout={checkout}&adult={adult}&children={children}&room_type={room_type}"
        return HttpResponseRedirect(url_with_params)

    # else:
    #     return redirect("hotel:index")
