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
from django.contrib.auth import authenticate, login, logout
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

    # form = UserRegisterForm(request.POST or None)
    context = {"form": form}
    return render(request, "userauths/sign-up.html", context)


def loginViewTemp(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('hotel:index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # To check if a user exist
            user_query = User.objects.get(email=email)   

            # for authentication, to log the user in
            user_auth = authenticate(request, email=email, password=password)

            if user_query is not None:
                login(request, user_auth)
                messages.success(request, "You are Logged In")
                # return redirect()
                next_url = request.GET.get("next", 'hotel:index')
                return redirect(next_url)

            else:
                messages.error(request, 'Username or password does not exit.')
                return redirect("userauths:sign-in")
        except:
            messages.error(request, 'User does not exist')
            return redirect("userauths:sign-in")


    return render(request, "userauths/sign-in.html")

def LogoutView(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect("userauths:sign-in")

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import HotelForm

@login_required
def add_hotel(request):
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
            form.save_m2m()  # Save the many-to-many data for tags
            messages.success(request, 'Hotel added successfully!')
            return redirect('hotel_list')  # Replace with your actual redirect target
        else:
            messages.error(request, 'Error adding hotel. Please check the form.')
    else:
        form = HotelForm()
    return render(request, 'hotel/hotelier_add_hotel.html', {'form': form})


