from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

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
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1']
            )
            auth.login(request, user)
            
            # Profile 정보만 업데이트 (생성은 signals.py에서 자동으로 처리됨)
            user.profile.birthdate = request.POST.get('birthdate')
            user.profile.job = request.POST.get('job')
            user.profile.nickname = request.POST.get('nickname')
            user.profile.save()

            return redirect('/')
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'register.html')