from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, AddRecord
from .models import Record

# Create your views here.


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
            messages.success(request, "You Have Registered Successfully!")
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
    

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_record = Record.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, "Record Deleted Successfully.")
        return redirect("home")
    else:
        messages.success(request, "You Must Be Logged In To Delete a Record.")
        return redirect("login")
    

def add_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            new_record = AddRecord(request.POST)
            if new_record.is_valid():
                new_record.save()
                messages.success(request, "New Record Added Successfully.")
                return redirect("home")
        else:
            new_record = AddRecord()
        context = {"new_record":new_record}
        return render(request, "add_record.html", context)
    else:
        messages.success(request, "You Must Be Logged In To Add a Record.")
        return redirect("login")
    

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        updated_record = AddRecord(request.POST, instance=current_record)
        if update_record.is_valid():
            update_record.save()
            messages.success(request, "Record Has Been Updated Successfully.")
            return redirect("home")
        context = {"updated_record":update_record}
        return render(request, "update_record.html", context)
    else:
        messages.success(request, "You Must Be Logged In To Add a Record.")
        return redirect("login")