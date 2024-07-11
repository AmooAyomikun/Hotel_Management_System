from django.urls import path,include 

from hotel import views

app_name = "hotel"

urlpatterns = [
    path("", views.index, name="index")
]