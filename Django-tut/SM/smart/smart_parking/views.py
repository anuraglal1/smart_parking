from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import time
from datetime import datetime, timedelta
import os
from pprint import pprint
from decimal import Decimal
from geoposition import Geoposition
from django.template import RequestContext
from elasticsearch import Elasticsearch,RequestsHttpConnection
import re
import boto3
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.core.exceptions import *
from geopy.geocoders import Nominatim
import uuid, OpenSSL
from smart_parking.models import slot,Order
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import datetime

#from .worker import Worker

'''host = ''#YOUR HOST
port = 443

#es = Elasticsearch()
es = Elasticsearch(
        hosts=[{'host': host,'port':port}],
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )

sqs = boto3.resource('sqs',region_name='us-west-2')
queue = sqs.get_queue_by_name(QueueName='parking_test')
client = boto3.client('sns',region_name="us-west-2")
worker = Worker()
client = boto3.client('sns',region_name="us-west-2")

#Find parking when asked for
@csrf_protect
def find_parking(request,radius=0.5):
    print(request.POST)
    if request.method == 'POST':
        if 'session_id' in request.POST:
            uuid_str = request.POST.get('session_id', '')
            uname = uuid_str.split('#')[1]
            if request.session.has_key(uname):
                if 'lat' in request.POST and 'long' in request.POST:
                    lat = str(request.POST.get('lat',''))
                    lon = str(request.POST.get('long',''))
                    if 'radius' in request.POST:
                        if request.POST.get('radius','') == '':
                            pass
                        else:
                            radius = request.POST.get('radius','')
                    parking_spots = records_in_radius(lat,lon,radius)
                    if parking_spots is not None:
                        print(parking_spots)
                        park_spots=parking_spots['hits']['hits']
                        spots=[]
                        for park_spot in park_spots:
                            source = park_spot.get('_source')
                            a={}
                            lat_obtained = source.get('location').get('lat')
                            lon_obtained = source.get('location').get('lon')
                            a['lat'] = source.get('location').get('lat')
                            a['lon'] = source.get('location').get('lon')
                            a['user'] = source.get('user')
                            """
                            address = rev_geocode(str(lat_obtained),str(lon_obtained))
                            if address is not None:
                                a['address'] = address
                            """
                            spots.append(a)
                        #return render(request,'findParking.html',{"spots":spots})
                        return JsonResponse({"spots":spots})
                    else:
                        return HttpResponse("Request error")
                else:
                    return HttpResponse("Latitude or Longitude missing")
            else:
                return render(request,"index.html")
        else:
            return render(request,"index.html")
    else:
        return render(request,"index.html")'''

'''def records_in_radius(lat,lon,radius):
    #Filter Query to be written. parking_spots contains the free slots 
    try:
        parking_spots=es.search(index='smart_test', body={"from" : 0, "size" :
            10000,"query": {"filtered": {"filter": 
                                        {
                                            "geo_distance": {
                                                "distance": str(radius)+"mi", 
                                                "location": { 
                                                    "lat": lat,
                                                    "lon": lon
                                                }
                                            }
                                        }
                                    }
                        }})
        return parking_spots
    except Exception as e:
        print(e)
        return None'''

#For the user to login
def login(request):
    print(request)
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = es.search(index='smart_user',doc_type='user_profile',body={"query": {"bool":
             {
                "should": [{ "match": { "username":  username }},
                            { "match": { "password": password }}
                        ]
                }
            }})
            user_hits = user['hits']['hits'] 
            if len(user_hits) == 0:
                return JsonResponse({"status":"No such user. Try again"})
            else:
                #Try for already logged in
                name = user_hits[0].get('_source').get('username')
                uuid_session = uuid.UUID(bytes = OpenSSL.rand.bytes(16))
                uuid_str_session = str(uuid_session)+'#'+name
                print(uuid_str_session)
                request.session[name]=uuid_str_session
                return JsonResponse({"status":"success","session_id":uuid_str_session})
        except Exception as e:
            print(e)
            return JsonResponse({"status":"No such user. Try again"})
    else:
        return render(request,"index.html")

#Call this to store in es and then render the other things
def register(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        password_test = password_check(password)
        ph_check = len(phone_number) == 10
        #user_username = User_Profile.objects.get(pk = username)
        user = es.search(index='smart_user',doc_type='user_profile',body={"query": 
            { "match":
                { 
                    "username":  username }
                }
        })

        user_hits = user['hits']['hits'] 
        print(user_hits)
        if len(user_hits) != 0:
            return JsonResponse({"status":"Username already exists"})
        elif password_test is False:
            return JsonResponse({"status":"Password must contain a number and" \
             " an alphanumeric character"})
        elif ph_check is False:
            return JsonResponse({"status":"Enter a valid Phone number"})
        else:
            doc = {
                    "password":password,
                    "phone_number":phone_number,
                    "points":str(100),
                    "username": username,
                    "timestamp":datetime.now() 
            }
            es.index(index='smart_user',doc_type='user_profile',id=id, body=doc)
            return JsonResponse({"status":"success"})
    else:
        return render(request,'register.html')


'''def logout(request):
    try:
        del request.session['username']
    except:
        pass
        return HttpResponse("<strong>You are logged out.</strong>")'''


def dashboard(request):
    #Get a GET Request
    '''if request.method == 'POST':
        try:
            if 'session_id' in request.POST:
                uuid_str = request.POST.get('session_id', '')
                uname = uuid_str.split('#')[1]
                if request.session.has_key(uname):
                    print("Dashboard "+uuid_str)
                    return render(request,'dashboard.html',{'session_id':uuid_str})
            else:
                return render(request,"index.html")
        except Exception as e:
            print(e)
            return render(request,"index.html")
    else:
    '''    
    return render(request,"dashboard.html")

def input(request):
    if request.method == 'POST':
        if 'session_id' in request.POST:
            uuid_str = request.POST.get('session_id', '')
            uname = uuid_str.split('#')[1]
            if request.session.has_key(uname):
                if 'lat' in request.POST and 'long' in request.POST:
                    lat = str(request.POST.get('lat', ''))
                    lon = str(request.POST.get('long', ''))
                    print('Lat and long are '+lat+' '+lon)
                    try:
                        doc = {
                            "location":{
                                "lat": lat, 
                                "lon": lon
                            },
                            "user": uname,
                            "timestamp":datetime.now() 
                        }
                        id = str(lat)+'#'+str(lon)
                        es.index(index='smart_test',doc_type='park',id=id, body=doc)
                        return render(request,"input.html",{'session_id':uuid_str})
                    except Exception as e:
                        print(e)
                        return HttpResponse("Could not Index the location ")
            else:
                return HttpResponse("NO lat or long")
        else:
            return render(request,"index.html")
    else:
        return render(request,"index.html")
    

def find(request):
    if request.method == 'POST':
        try:
            if 'session_id' in request.POST:
                uuid_str = request.POST.get('session_id', '')
                uname = uuid_str.split('#')[1]
                if request.session.has_key(uname):
                    print("Dashboard "+uuid_str)
                    return render(request,'findParking.html',{'session_id':uuid_str})
            else:
                return render(request,"index.html")
        except Exception as e:
            print(e)
    else:
        return render(request,"index.html")

def delete_parking(request): #Accept Geocoded address
    if request.method == 'POST':
        if 'session_id' in request.POST:
            uuid_str = request.POST.get('session_id', '')
            uname = uuid_str.split('#')[1]
            if request.session.has_key(uname):
                if 'lat' in request.POST and 'long' in request.POST:
                    lat = str(request.POST.get('lat', ''))
                    lon = str(request.POST.get('long', ''))
                    #address = str(request.POST.get('address', ''))
                    try:
                        id = lat+'#'+lon
                        delete = es.delete(index='smart_test',doc_type='park',id=id)
                        print(delete)
                        if delete.get('found') == True:
                            try:
                                queue.send_message(MessageBody=uname, MessageAttributes={
                                    'id':{
                                        'StringValue': id,
                                        'DataType': 'String'
                                    }
                                })
                                worker.thread_pool()
                            except Exception as e:
                                print('Exception in msg '+str(e))
                            return JsonResponse({"spot":"success"})
                        else:
                            return JsonResponse({"spot":"failure"})
                    except Exception as e:
                        print(e)
                        return HttpResponse("Could not Index the location")
                else:
                    return HttpResponse("NO lat or long")
            else:
                return render(request,"index.html")
        else:
            return render(request,"index.html")
    else:
        return render(request,'input.html')



def password_check(password):
    # calculating the length
    length_error = len(password) < 5

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"\w", password) is None

    # overall result
    password_ok = not ( length_error or digit_error or lowercase_error )

    return password_ok

'''def logout(request):
    if request.method == 'POST':
        if 'session_id' in request.POST:
            uuid_str = request.POST.get('session_id', '')
            uname = uuid_str.split('#')[1]
            if request.session.has_key(uname):      
                try:
                    del request.session[uname]
                except:
                    pass
        return render(request,"index.html")
    else:
        return render(request,"index.html")'''

def input_html(request):
    if request.method == 'POST':
        try:
            if 'session_id' in request.POST:
                uuid_str = request.POST.get('session_id', '')
                uname = uuid_str.split('#')[1]
                if request.session.has_key(uname):
                    print("Input is "+uuid_str)
                    return render(request,'input.html',{'session_id':uuid_str})
            else:
                return render(request,'input.html')
        except Exception as e:
            print(e)
    else:
        return render(request,"index.html")

def home(request):
 	return render(request,"input.html")

def bookyourslot(request):
	return render(request,"booked.html")

def cancelyourslot(request):
    return render(request,"cancel.html")

def all_slots(request):
    a=slot.objects.all()
    return render(request,"all_slots.html",{'a': a})

#@login_required
def book_slot(request):
    if request.POST:
        form = OrderForm(request.POST)
        if form.is_valid():
            if form.save():
                a=slot.objects.all(id=1)
                a.slot_status="Booked"
                return redirect('/', messages.success(request, 'Order was successfully created.', 'alert-success'))
            else:
                return redirect('/', messages.error(request, 'Data is not saved', 'alert-danger'))
        else:
            return redirect('/', messages.error(request, 'Form is not valid', 'alert-danger'))
    else:
        form = OrderForm()
        return render(request, 'book_slot.html', {'form':form})

def show(request):
    a=Order.objects.get(id=1)
    start=a.start_time
    end=a.end_time
    startdelta=datetime.timedelta(hours=start.hour,minutes=start.minute,seconds=start.second)
    enddelta=datetime.timedelta(hours=end.hour,minutes=end.minute,seconds=end.second)
    x=(enddelta-startdelta).seconds/60
    x=x/60
    y=x*20
    d=datetime.datetime.now()
    #return render(request,"input.html")
    return render(request,"show.html",{'a':a,'x':x,'y':y,'d':d})

