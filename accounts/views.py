from django.http import response,HttpResponseRedirect
from Blogmain.settings import SECRET_KEY
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
import json
import requests
from django.core.mail import EmailMessage
from django.conf import settings



def signup(request):

    if request.method=='POST':

        verify=googlecaptcha(request)

        if(verify==True):

            username=request.POST['name']
            email=request.POST['email']
            password=request.POST['pass']
            re_pass=request.POST['re_pass']

            if(re_pass==password and User.objects.filter(username=username).exists()==False and User.objects.filter(email=email).exists()==False):
                        user = User.objects.create_user(username=username,email=email,password=password)
                        user.save()
                        return redirect('login')
            else:
                messages.info(request,"invalid creditials")
                return render(request,'signup.html')
        else:
            messages.info(request,"Please attempt Captcha")
            return render(request,'signup.html')

    else:    
        return render(request,'signup.html')

def login(request):

    if request.method=='POST':

        verify=googlecaptcha(request)

        if(verify==True):

            username=request.POST['name']
            password=request.POST['pass']
            user =auth.authenticate(username=username,password=password) 

            if user is not None:
                auth.login(request,user)
                return redirect("/")

            else:
                messages.info(request,"invaild username or password")
                return render(request,"login.html") 
 
        else:
            messages.info(request,"Please attempt Captcha")
            return render(request,'login.html')

    else:    
        return render(request,'login.html')

def logout(request):

    if User.is_authenticated:
        auth.logout(request)
        return redirect("/")

def googlecaptcha(request):

        clientkey=request.POST['g-recaptcha-response']
        secret_key="6LfYA9YaAAAAANTYB40wFiLJiNz90EHm0l5SV7XB"

        captcha={
            'secret':secret_key,
            'response': clientkey
        }

        r = requests.post("https://www.google.com/recaptcha/api/siteverify",data=captcha)
        Gresponse=json.loads(r.text)
        verify=Gresponse['success']

        return verify

def email(request):
    email = EmailMessage('Hello', 'World',settings.EMAIL_HOST_USER,['virufaldu672002@gmail.com'])
    email.fail_silently=True
    email.send()
    return render(request,'email.html');