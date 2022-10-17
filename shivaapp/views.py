from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseGone, HttpResponseRedirect
from django.core.mail import send_mail
import math, random
from .forms import CityForm
from .models import City
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User




OTP={
    
}

def home(request):
    return render(request, "home.html")


def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP




def send_otp(request):
    email=request.POST.get("email")
    print(email)

    o=generateOTP()
    print(o)
    OTP.update({
        email:o
    })
    try:
        user,created = User.objects.get_or_create(
            email=email,
            username=email
        )
        print(user)
        if created:
            user.set_password('secret')
            user.save()
    except Exception as ee:
        pass

    send_mail('OTP request',f'your OTP is {o}','testsmtpintelsafe@gmail.com',[email], fail_silently=False,)
    print(o)
    return HttpResponse(o)
     # except Exception as e:
     #      return 'unable to send otp ',500
     
     
def logoutUser(request):
    logout(request)
    return redirect("home")


def auth(request):
    email = request.POST.get('email')
    print(email)

    user = authenticate(request,username=email,password='secret')
    print(user)
    if user is not None:
        login(request,user)
        return redirect('weather')
    return HttpResponse("don't try to act smart!!! this is an authenticated project!!!!!")


@login_required     
def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        #json parsing
        r = requests.get(url.format(city)).json()   


        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class
    }

    return render(request, 'weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    
    return redirect('weather')