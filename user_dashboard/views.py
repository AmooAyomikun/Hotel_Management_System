from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from hotel.models import Booking, Notification, Bookmark, Hotel, Review
from userauths.models import Profile, User
from userauths.forms import ProfileUpdateForm, UserUpdateForm



# @login_required
# def dashboard(request):
#     bookings = Booking.objects.filter(user=request.user, payment_status="paid")
#     total_spent = Booking.objects.filter(user=request.user, payment_status="paid").aggregate(amount=models.Sum('total'))

#     print("bookings ========", total_spent)
#     context = {
#         "bookings":bookings,
#         "total_spent":total_spent,
#     }
#     return render(request, "user_dashboard/dashboard.html", context)

@login_required
def dashboard(request):
    bookings = Booking.objects.filter(user=request.user)
    total_spent = Booking.objects.filter(user=request.user).aggregate(amount=models.Sum('total'))
    # total_spent_amount = total_spent['amount'] if total_spent['amount'] is not None else 0
    
    # if request.user =="POST":
    print(f"bookings: {bookings.count}")
    print(f"total_spent: {total_spent}")
# Handle None value for total_spent

    context = {
        "bookings": bookings,
        "total_spent": total_spent,  # pass the checked amount
    }
    return render(request, "user_dashboard/dashboard.html", context)

@login_required
def bookings(request):
    bookings = Booking.objects.filter(user=request.user, payment_status="paid")
    print(bookings)

    context = {
        "bookings":bookings,
    }
    return render(request, "user_dashboard/bookings.html", context)

@login_required
def booking_detail(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id, user=request.user, payment_status="paid")

    context = {
        "booking":booking,
    }
    return render(request, "user_dashboard/booking_detail.html", context)

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user, seen=False)

    context = {
        "notifications":notifications,
    }
    return render(request, "user_dashboard/notifications.html", context)

def notification_mark_as_seen(request, id):
    # id = request.GET['id']
    noti = Notification.objects.get(id=id)
    noti.seen = True
    noti.save()
    messages.success(request, "Notification Seen")
    return redirect("user_dashboard:notifications")

@login_required
def wallet(request):
    bookings = Booking.objects.filter(user=request.user, payment_status="paid")
    total_spent = Booking.objects.filter(user=request.user, payment_status="paid").aggregate(amount=models.Sum('total'))
    wallet_balance = request.user.profile.wallet

    context = {
        "bookings":bookings,
        "total_spent":total_spent,
        "wallet_balance": wallet_balance,
    }
    return render(request, "user_dashboard/wallet.html", context)

@login_required
def bookmark(request):
    bookmark = Bookmark.objects.filter(user=request.user)
    return render(request, "user_dashboard/bookmark.html", {"bookmark":bookmark,})

@login_required
def delete_bookmark(request, bid):
    bookmark = Bookmark.objects.filter(bid=bid)
    bookmark.delete()
    messages.success(request, "Bookmark Deleted")
    return redirect("user_dashboard:bookmark")

def add_to_bookmark(request):
    id = request.GET.get('id')
    hotel = Hotel.objects.get(id=id)
    if request.user.is_authenticated:
        bookmark = Bookmark.objects.filter(user=request.user, hotel=hotel)
        if bookmark.exists():
            bookmark = Bookmark.objects.get(user=request.user, hotel=hotel)
            bookmark.delete()
            return JsonResponse({"data":"Bookmark Deleted", "icon":"success"})
        else:
            Bookmark.objects.create(user=request.user, hotel=hotel)
            return JsonResponse({"data":"Hotel Bookmarked" , "icon":"success"})
    else:
        return JsonResponse({"data":"Login To Bookmark Hotel" , "icon":"warning"})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect("user_dashboard:profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "profile":profile,
        "u_form":u_form,
        "p_form":p_form,
    }
    return render(request, "user_dashboard/profile.html", context)

@login_required
def password_changed(request):
    return render(request, "user_dashboard/password-changed.html")

@login_required
def add_review(request):
    id = request.GET['id']
    rating = request.GET['rating']
    review = request.GET['review']
    hotel = Hotel.objects.get(id=id)

    review_check = Review.objects.filter(user=request.user, hotel=hotel)
    if review_check.exists():
        return JsonResponse({"data":"Review Already Exists", "icon":"warning"})
    else:
        Review.objects.create(
            user=request.user,
            rating=rating,
            hotel=hotel,
            review=review
        )
        return JsonResponse({"data":"Review Submitted, Thank You." , "icon":"success"})


