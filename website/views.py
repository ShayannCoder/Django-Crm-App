from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def home(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"] 
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged in")
            return redirect("home")
        else:
            messages.success(request, "There Was an Error Logging in, Please Try Again")
            return redirect("home")
    else:
         return render(request, "home.html")