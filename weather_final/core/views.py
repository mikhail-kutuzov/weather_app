from django.shortcuts import render
from .models import City
# Create your views here.


def get_html_content(city):
    import requests
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = city.replace(" ", "+")
    html_content = session.get(f'https://www.google.co.uk/search?q=weather+in+{city}').text
    return html_content


def home(request):
    import requests
    import json
    from datetime import datetime, timedelta
    import calendar

    #time date
    tl=datetime.today()
    td=tl
    #default location delhi
    city='New Delhi'
    resp=requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=a286d2cdc0d8a14c153ed08bf2339c1d')
    data= resp.json()
    diff=data['timezone']
    currt= td.hour*3600 + td.minute*60 + td.second+diff #-19800 commented
    dtlist=adjuster(currt,td)
    _hour=dtlist[1]
    _mint=dtlist[2]
    _date=dtlist[0]
    wekday = calendar.day_name[_date.weekday()]
    month=_date.strftime("%b")
    result={'region':data['name'],'winder':int(3.6*data['wind']['speed'] + 0.5),'temp_now':int(data['main']['temp'])-273,'weather_now':data['weather'][0]['description'],'cuntry':data['sys']['country'],'humid':data['main']['humidity'],'visible':data['visibility']/100,'rel':0,'hours':_hour,'minutes':_mint,'weekday':wekday,'mon':month,'day':_date.day}   
    if 'city' in request.GET:
       city =request.GET.get('city')
       temp = saver(request)
       resp = requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=a286d2cdc0d8a14c153ed08bf2339c1d')
       data = resp.json()

       if data['cod']=='404':
          city='New Delhi'
          resp=requests.get('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=a286d2cdc0d8a14c153ed08bf2339c1d')
          data= resp.json()
          result={'region':data['name'],'winder':int(3.6*data['wind']['speed'] + 0.5),'temp_now':int(data['main']['temp'])-273,'weather_now':data['weather'][0]['description'],'cuntry':data['sys']['country'],'humid':data['main']['humidity'],'visible':data['visibility']/100,'rel':1,'hours':_hour,'minutes':_mint,'weekday':wekday,'mon':month,'day':_date.day}   

       else:
           diff=data['timezone']
          # tarik=td
           currt= td.hour*3600 + td.minute*60 + td.second+diff #-19800 commented
           dtlist=adjuster(currt,td)
           _hour=dtlist[1]
           _mint=dtlist[2]
           _date=dtlist[0]
           wekday = calendar.day_name[_date.weekday()]
           month=_date.strftime("%b")      
           result={'region':data['name'],'winder':int(3.6*data['wind']['speed'] + 0.5),'temp_now':int(data['main']['temp'])-273,'weather_now':data['weather'][0]['description'],'cuntry':data['sys']['country'],'humid':data['main']['humidity'],'visible':data['visibility']/100,'rel':0,'hours':_hour,'minutes':_mint,'weekday':wekday,'mon':month,'day':_date.day}   
    
    if data['weather'][0]['main']=='Clouds':
        return render(request, 'core/cloudy.html', {'result': result})

    if (data['weather'][0]['main']=='Rain') or (data['weather'][0]['main']=='Drizzle'):
        result={'region':data['name'],'winder':int(3.6*data['wind']['speed'] + 0.5),'temp_now':int(data['main']['temp'])-273,'weather_now':data['weather'][0]['description'],'cuntry':data['sys']['country'],'humid':data['main']['humidity'],'visible':data['visibility']/100,'precip':data['rain']['1h'],'rel':0,'hours':_hour,'minutes':_mint,'weekday':wekday,'mon':month,'day':_date.day}   
        return render(request, 'core/rainy.html', {'result': result})    

    if data['weather'][0]['main']=='Clear':
        return render(request, 'core/sunny.html', {'result': result})    

    if (data['weather'][0]['main']=='Haze') or (data['weather'][0]['main']=='Mist') or (data['weather'][0]['main']=='Fog'):
        return render(request, 'core/haze.html', {'result': result})    

    if data['weather'][0]['main']=='Snow':
        result={'region':data['name'],'winder':int(3.6*data['wind']['speed'] + 0.5),'temp_now':int(data['main']['temp'])-273,'weather_now':data['weather'][0]['description'],'cuntry':data['sys']['country'],'humid':data['main']['humidity'],'visible':data['visibility']/100,'precip':data['snow']['1h'],'rel':0,'hours':_hour,'minutes':_mint,'weekday':wekday,'mon':month,'day':_date.day}   
        return render(request, 'core/snowy.html', {'result': result})

    if (data['weather'][0]['main']=='Thunderstorm') or (data['weather'][0]['main']=='Squall') or (data['weather'][0]['main']=='Tornado'):
        return render(request, 'core/windy.html', {'result': result})    

    if (data['weather'][0]['main']=='Dust') or (data['weather'][0]['main']=='Sand') or (data['weather'][0]['main']=='Ash') or (data['weather'][0]['main']=='Smoke'):
        return render(request, 'core/dusty.html', {'result': result})  

    return render(request, 'core/sunny.html', {'result': result})

def saver(request):
    city=request.GET.get('city')
    town = City(name=city)
    town.save()
    return 10

def history(request): 
    return render(request,'core/history.html',{'cities':City.objects.all()})

def adjuster(currt,tarik):
    from datetime import datetime, timedelta
    import calendar

    if(currt<0):
        tarik=tarik-timedelta(1)
        currt+=86400
        ghante=currt/3600
        ghante=int(ghante)
        currt=currt%3600
        mint=currt/60
        mint=int(mint)

    elif(currt>86400):
        tarik=tarik+timedelta(1)
        currt=currt-86400
        ghante=currt/3600
        ghante=int(ghante)
        currt=currt%3600
        mint= currt/60
        mint=int(mint)

    else:
        ghante=currt/3600
        ghante=int(ghante)
        currt=currt%3600
        mint=currt/60
        mint=int(mint)
    
    if ghante<10 :
        ghante='0'+str(ghante)

    if mint<10 :
        mint='0'+str(mint)    
    datime = [tarik,ghante,mint]
    return(datime)

