from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm

def loginpage(request):
    print(request.method)
    if request.method == 'POST':
        username,password=request.POST.get('username'),request.POST.get('password')
        user=authenticate(request=request,username=username,password=password)
        if user:
            login(request,user)
    if request.user.is_authenticated:
        return render(request,"home.html",{'username':request.user.username})
    return render(request, 'login.html', {'form': LoginForm})

def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("loginurl")

        

# Create your views here.
