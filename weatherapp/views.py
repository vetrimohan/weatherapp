from django.shortcuts import render
from django.shortcuts import redirect

from .forms import Cityform

from django.contrib import messages
from .models import City
import requests



def home(request):

    url="https://api.openweathermap.org/data/2.5/weather?q={}&appid=71608e0a648a39cf75dc17a35c06881d&units=metric"
    

    if request.method=="POST":
        
        form=Cityform(request.POST)
        if form.is_valid():
            ncity=form.cleaned_data['name']
            ccity=City.objects.filter(name=ncity).count()
            if ccity==0:
                res=requests.get(url.format(ncity)).json()
                print(res)
                if res['cod']==200:
                    print(res)
                    form.save()
                    messages.success(request,'data added successfully')
                else:

                    messages.error(request,'data does not exist')
            else:
                messages.error(request,'data already exists')
        
    form=Cityform()
    cities=City.objects.all()
    weather_report=[]
    for wcity in cities:

        res=requests.get(url.format(wcity)).json()
        print(res)
        weather_city={
            "city":wcity,
            "temperature" : res['main']['temp'],
            "description" : res['weather'][0]['description'],
            'country' : res['sys']['country'],
            'icon' :res['weather'][0]['icon']


        }
        weather_report.append(weather_city)
       





    return render(request,'weathersapp.html',{'weather_report':weather_report,"form":form})
def delete_city(request,city):

    
    if request.method=='POST':
        city_obj = City.objects.get(name=city)
        city_obj.delete()
        messages.success(request,'City deleted successfully')
    return redirect('home')