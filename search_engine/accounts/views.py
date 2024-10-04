from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', context={"login_form":form})

def register_request(request):
    if request.method == "POST":
        if request.POST['password1']==request.POST['password2']:
            user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            auth.login(request,user)
            return redirect('/')
    return render(request,'register.html')