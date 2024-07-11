# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib import messages
# from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import logout
# from django.contrib.auth.decorators import login_required

# # Create your views here.
# from userauths.models import User, profile
# from userauths.forms import UserRegisterForm

# def RegisterView(request):
#     if request.user.is_authenticated:
#         messages.warning(request, f"You are already logged in.")
#         return redirect('hotel:index')

#     form = UserRegisterForm(request.POST or None)
     
#     if form.is_valid():
        
#         full_name = form.cleaned_data.get("full_name")
#         phone = form.cleaned_data.get("phone")
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password1")
#         form.save()

#         user = authenticate(email=email, password=password)
#         login(request,user)
#         messages.success(request, f"Hey {full_name} your account has been created successfully")

#         profile = Profile.objects.get(user=request.user)
#         profile.full_name = full_name
#         profile.phone = phone
#         profile.save()

#         return redirect("hotel:index")

#     context = { 
#         "form":form
#     }
#     return render(request, "userauths/sign-up.html", context)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Import the models and forms
from userauths.models import User, Profile
from userauths.forms import UserRegisterForm

def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('hotel:index')

    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()

        # Authenticate and login the user
        login(request, user)
        messages.success(request, f"Hey {user.full_name}, your account has been created successfully")

        # Create and update the profile
        profile = Profile.objects.get(user=user)
        profile.full_name = user.full_name
        profile.phone = user.phone
        profile.save()

        return redirect('hotel:index')

    context = {"form": form}
    return render(request, "userauths/sign-up.html", context)



