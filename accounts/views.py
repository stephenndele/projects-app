from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from main.email import send_welcome_email



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
            user = form.save()

            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=user.username, password=raw_password)
            name = request.POST["username"]
            email = request.POST["email"]
            send_welcome_email(name,email)
            login(request, user)

            return redirect("main:home")

    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


    #   check credentials  
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)
                return redirect('main:home')
            else:
                return render(request, 'accounts/login.html', {"error": "Your accout id is not active"})

        else:
            return render(request, 'accounts/login.html', {"error": "Invalid username or password"})

    return render(request, 'accounts/login.html')

def logout_user(request):
    logout(request)
    return redirect('accounts:login')