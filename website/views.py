from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    return render(request, "home.html")


def login_user(request):
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
            return redirect("login")
    else:
         return render(request, "login.html")
    

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out")
    return redirect("login")