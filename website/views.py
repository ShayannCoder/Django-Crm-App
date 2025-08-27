from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import Record

# Create your views here.

@login_required
def home(request):
    records = Record.objects.all()
    context = {"records":records}
    return render(request, "home.html", context)


def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered!")
            return redirect("home")
    else:
        form = UserRegistrationForm()
    context = {"form":form}
    return render(request, "register.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"] 
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged in.")
            return redirect("home")
        else:
            messages.success(request, "There Was an Error Logging in, Please Try Again.")
            return redirect("login")
    else:
         return render(request, "login.html")
    

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out.")
    return redirect("login")


def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        context = {"record":record}
        return render(request, "customer_record.html", context)
    else:
        messages.success(request, "You Must Be Logged In To View That Page.")
        return redirect("login")