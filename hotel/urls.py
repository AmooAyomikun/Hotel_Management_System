from django.urls import path,include 

from hotel import views

app_name = "hotel"

urlpatterns = [
    path("", views.index, name="index"),
    path("detail/<slug:slug>/", views.hotel_detail, name="hotel_detail"),
    path("detail/<slug:slug>/room-type/<slug:rt_slug>/", views.room_type_detail, name="room_type_detail"),
    path("selected_rooms/", views.selected_rooms,name="selected_rooms"),
    path("checkout/<booking_id>/", views.checkout, name="checkout"),
    path("update_room_status/", views.update_room_status, name="update_room_status"),
    path("hotelier_add_hotel/", views.hotelier_add_hotel, name="hotelier_add_hotel"),
    path('search-hotels/', views.search_hotels_view, name='hotel_hotels'),

    # Payment Routes
    path('api/create_checkout_session/<booking_id>/', views.create_checkout_session, name='api_checkout_session'),
    path('success/<str:booking_id>/', views.payment_success, name='success'),
    path('failed/<booking_id>/', views.payment_failed, name='failed'),
]