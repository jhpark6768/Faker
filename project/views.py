from django.shortcuts import redirect, render
from django.contrib.auth.models import User

def img(request):
    return render(request, 'image.html')

def index(request):
    return render(request, 'index.html')

def createAccount(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        
        return redirect("login")

def myinfo(request):
    if request.method == "GET":
        # request.user : 객체 
        userinfo = User.objects.get(username=(request.user.username))
        context = {
            "user" : userinfo
        }
        return render(request, 'registration/myinfo.html', context)
    else :
        userinfo = User.objects.get(username=(request.user.username))
        
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")

        if password != "":
            userinfo.set_password(password)
        userinfo.first_name = first_name
        userinfo.last_name = last_name
        userinfo.email = email

        userinfo.save()

        return redirect("/index")

def withdraw(request):
    context = {
        "user" : request.user.username
    }
    User.objects.get(username=(request.user.username)).delete()
    return render(request, 'registration/withdraw.html', context)