from tkinter.tix import INTEGER
from numpy import generic
from account.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from django.contrib.auth import authenticate,login,logout
from django.http import FileResponse, HttpResponseRedirect, HttpResponse



def home(request):
    return render(request, 'home.html')

def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'Utilisateur introuvable.')
            return redirect('/user/accounts/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'votre profile n est pas encore activer.')
            return redirect('/user/accounts/login')

        user = authenticate(request, username = username , password = password)
        login(request, user)
        if user is None:
            messages.success(request, 'Mot de passe incorrect.')
            return redirect('/user/accounts/login')
        
        if(profile_obj.type == 1 ):
            login(request , user)
            return redirect('/agent_index')
        
        if(profile_obj.type == 3):
            login(request, user)
            return redirect('/admin_index')
        
        else:
            login(request, user)
            return redirect('/')

    return render(request , 'login.html')

def error_page(request):
    return  render(request , 'error.html')


def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, "l'email de verification a ete envoyer.")
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Votre compte est activer avec succes.')
            return redirect('/user/accounts/login')
        else:
            return redirect('/user/error')
    except Exception as e:
        print(e)
        return redirect('/')


def success(request):
    return render(request , 'success.html')


def token_send(request):
    return render(request , 'token_send.html')


def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        raison = request.POST.get('raison')
        telephone = request.POST.get('telephone') 
        
       
        print(password)
        print(telephone)
        print(raison)

        if (username =="" or password=="" or email==""):
            messages.success(request, "renseigner tous les champs")
            return redirect('/user/register')

        else:
            try:

                if User.objects.filter(username = username).first():
                    messages.success(request, "Le nom d'utilisateur est deja pris")
                    return redirect('/user/register')

                if User.objects.filter(email = email).first():
                    messages.success(request, "l'email existe deja")
                    return redirect('/user/register')
                
                else:

                    if(raison==""):
                        user_obj = User(username = username , email = email)
                        user_obj.set_password(password)
                        user_obj.save()
                        auth_token = str(uuid.uuid4())
                        profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token,)
                        profile_obj.save()
                    
                        send_mail_after_registration(email , auth_token)
                        return redirect('/user/token')


                    else:
                        user_obj = User(username = username , email = email)
                        user_obj.set_password(password)
                        user_obj.save()
                        auth_token = str(uuid.uuid4())
                        tel = telephone
                        rais = raison
                        print(tel)
                        print(rais)
                        profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token, type=1, telephone = tel, raison=rais )
                        profile_obj.save()

                        send_mail_after_registration(email , auth_token)
                        return redirect('/user/token')

            except Exception as e:
                print(e)


    return render(request , 'register.html')


def send_mail_after_registration(email , token):
    subject = 'votre compte va etre verifier consulter votre boite mail'
    message = f'Bonjour voicie le lien pour activer votre compte http://127.0.0.1:8000/user/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


