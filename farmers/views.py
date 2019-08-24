from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from datetime import datetime
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from farmers.models import Farmer,Enquiry,Chat,Experts,AddYield
import urllib.request, json
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
import pickle
from sklearn.externals import joblib
from sklearn import linear_model

def home(request):
    return render(request,'farmers/home.html')

def f_signup(request):
    return render(request,'farmers/farmer-signup.html')

def f_login(request):
    return render(request,'farmers/farmer-login.html')

def chat_box_list(request,username1):
    username=request.session['username']
    f_uname=username1
    request.session['msgto']=f_uname

    f = Farmer.objects.filter(username=f_uname)
    if len(f):
        f=Chat.objects.filter(fromm=username,to=f_uname )| Chat.objects.filter(fromm=f_uname,to=username).order_by('current_time')
        return render(request,'farmers/chat_screen.html',{'username':username,'f_username':f_uname,'chats':f})
    else:
        return HttpResponseRedirect(reverse('message_farmer'))
def farmer_signup_action(request):
    name=request.POST.get('name','NULL')
    email=request.POST.get('email','NULL')
    contact=request.POST.get('contact','NULL')
    username=request.POST.get('username','NULL')
    password=request.POST.get('password','NULL')
    village=request.POST.get('village','NULL')
    if 'wheat' in request.POST:
        crop='wheat'
    else:
        crop='crop'
    uploadedfileurl=''
    if request.method=='POST' and request.FILES['myfile']:
        myfile=request.FILES['myfile']
        fs=FileSystemStorage()
        filename=fs.save(myfile.name,myfile)
        uploadedfileurl=fs.url(filename)

    bool=usernamepresent(username)
    if contact=='NULL':
        contact=0
    if crop=='crop':
        return HttpResponse('Select crop')
    if bool==True:
        s=Farmer(name=name,email=email,contact=contact,username=username,password=password,village=village,grain=crop,pic_url=uploadedfileurl)

        s.save()
        if s.id:

            return HttpResponseRedirect(reverse('farmer-login'))
        else:
            return HttpResponse('Error')

    else:
        return HttpResponseRedirect(reverse('farmer-signup')+'?auth1=true')
        #return render(request,'student/register.html')

def usernamepresent(username):
    if Farmer.objects.filter(username=username).exists():
        return False
    else:
        return True


def farmer_login_action(request):
        username=request.POST['username']
        password=request.POST['password']

        l=Farmer.objects.filter(username=username,password=password)
        e=Experts.objects.filter(e_password=password,e_uname=username)

        if len(l):
            request.session['username']=username #session started
            return HttpResponseRedirect(reverse('farmer_profile'))

        elif len(e):
            status=0
            request.session['username']=username
            c=Enquiry.objects.filter(status=status)
            return render(request,'farmers/expert_page.html',{
                'enquiries':c,'expertname':username
            })

        else:
            return HttpResponseRedirect(reverse('farmer-login')+'?login_failure=true')

def farmer_profile(request):
    username=request.session['username']
    f = Farmer.objects.get(username=username)
    with urllib.request.urlopen("https://api.thingspeak.com/channels/660112/feeds.json?api_key=HPGVLWG9ICUIEJX1&results=1") as url:
        data = json.loads(url.read().decode())
        temp=data['feeds'][0]['field1']
        humd=data['feeds'][0]['field2']
    t=float(temp)
    h=float(humd)
    filename = '/Users/samdharsikumar/Desktop/tcet_hack/finalized_model.joblib'
    reg= joblib.load(filename)
    print(type(t))
    print(type(h))
    y=reg.predict([[t,h]])
    yy=y[0]
    yyy=round(yy,2)
    with urllib.request.urlopen("https://api.thingspeak.com/channels/660572/feeds.json?api_key=46JO8K7DKO2F6MX4&results=1") as url1:
        data1 = json.loads(url1.read().decode())
        soilm=data1['feeds'][0]["field3"]



    return render(request,'farmers/profile.html',{
        'farmer':f,'temp':temp,'humd':humd,'yield':yyy,'sm':soilm,

    })

def farmer_profile_view(request,username):
    #username=request.session['username']
    f = Farmer.objects.get(username=username)
    with urllib.request.urlopen("https://api.thingspeak.com/channels/660112/feeds.json?api_key=HPGVLWG9ICUIEJX1&results=1") as url:
        data = json.loads(url.read().decode())
        temp=data['feeds'][0]['field1']
        humd=data['feeds'][0]['field2']
    t=float(temp)
    h=float(humd)

    filename = 'C:/Users/hp/Desktop/finalized_model.joblib'
    reg= joblib.load(filename)
    print(type(t))
    print(type(h))
    y=reg.predict([[t,h]])
    yy=y[0]
    yyy=round(yy,2)
    with urllib.request.urlopen("https://api.thingspeak.com/channels/660572/feeds.json?api_key=46JO8K7DKO2F6MX4&results=1") as url1:
        data1 = json.loads(url1.read().decode())
        soilm=data1['feeds'][0]["field3"]

    return render(request,'farmers/profile_view.html',{
        'farmer':f,'temp':temp,'humd':humd,'yield':yyy,'sm':soilm,

    })


def farmer_logout(request):
    request.session.flush()

    return HttpResponseRedirect(reverse('farmer-login'))

def farmer_list(request):
    username=request.session['username']
    f = Farmer.objects.all()

    return render(request,'farmers/farmers_list.html',{
    'farmer':f,
    })


def view_enquiry(request):
    username=request.session['username']
    e = Enquiry.objects.filter(farmer_name=username)

    return render(request,'farmers/view_enquiry.html',{'enq':e,})


def enquire_experts(request):
    username=request.session['username']
    return render(request,'farmers/enquire_experts.html')

def enquire_experts_action(request):
    username=request.session['username']
    title=request.POST['title']
    desc=request.POST['desc']
    status=0
    e=Enquiry(farmer_name=username,desc=desc,title=title,status=status)
    e.save()

    return HttpResponseRedirect(reverse('farmer_profile'))

def message_farmer(request):
    return render(request,'farmers/message_farmer.html')

def chat_box(request):
    username=request.session['username']
    f_uname=request.POST['f_uname']
    request.session['msgto']=f_uname

    f = Farmer.objects.filter(username=f_uname)
    if len(f):
        f=Chat.objects.filter(fromm=username,to=f_uname )| Chat.objects.filter(fromm=f_uname,to=username).order_by('current_time')
        return render(request,'farmers/chat_screen.html',{'username':username,'f_username':f_uname,'chats':f})
    else:
        return HttpResponseRedirect(reverse('message_farmer'))

def chat_screen(request):
    return render(request,'farmers/chat_screen.html')

def on_chat_submit(request):
    f_uname=request.session['msgto']
    username=request.session['username']
    msg=request.POST['msg']
    c=Chat(fromm=username,to=f_uname,msg=msg)
    c.save()

    f = Farmer.objects.filter(username=f_uname)
    if len(f):
        f=Chat.objects.filter(fromm=username,to=f_uname )| Chat.objects.filter(fromm=f_uname,to=username).order_by('current_time')
        return render(request,'farmers/chat_screen.html',{'username':username,'f_username':f_uname,'chats':f})

def on_submit_solution(request):
    f_name=request.POST['f_name']
    username=request.session['username']
    title=request.POST['title']
    enquiry=request.POST['enquiry']
    solution=request.POST['solution']
    Enquiry.objects.filter(title=title,desc=enquiry,farmer_name=f_name).update(status=1,solution=solution)

    c=Enquiry.objects.filter(status=0)
    return render(request,'farmers/expert_page.html',{
        'enquiries':c,'expertname':username
    })


def view_submitted_solution_expert(request):
    username=request.session['username']
    c=Enquiry.objects.filter(status=1)
    return render(request,'farmers/view_submitted_solution_expert.html',{
    'enquiries':c,'expertname':username
    })

def pending_enq_from_solved(request):
    status=0
    username=request.session['username']
    c=Enquiry.objects.filter(status=status)
    return render(request,'farmers/expert_page.html',{
        'enquiries':c,'expertname':username
    })

def add_yield(request):
    return render(request,'farmers/add_yield.html')

def add_yield_action(request):
    username=request.session['username']
    monthh=request.POST['monthh']
    yearr=request.POST['yearr']
    yieldd=request.POST['yieldd']
    y=AddYield(f_uname=username,date=monthh,year=yearr,yieldd=yieldd)
    y.save()
    return HttpResponseRedirect(reverse('farmer_profile'))
