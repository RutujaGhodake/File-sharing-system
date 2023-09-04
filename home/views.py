from tkinter import E
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .serializers import *
from rest_framework.parsers import MultiPartParser


def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 == pass2:
            try:
                user = User.objects.get(username=uname)
                messages.info(request, 'Username already exists',extra_tags="sign3")
            except User.DoesNotExist:
                if ('@' or '!' or '#' or '$' or '%' or '^' or '&' or '*') not in pass1:
                    messages.info(request,'Password must contain atleast 1 special character',extra_tags="sign4")
                else:
                    myuser = User.objects.create_user(uname, email, pass1)
                    myuser.save()
                    messages.success(request, 'Account is created successfully', extra_tags="sign1")
                    return redirect('Login')
        else:
            messages.info(request, 'Your password and confirm password are not same!!',extra_tags="sign2")
    return render(request, 'signup.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
                login(request, user)
                return redirect('home')
        else:
            messages.info(request,'Username or password is not correct',extra_tags="log")
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('Login')

def home(request):
    return render(request, 'home.html')


def download(request, uid):
    return render(request, 'download.html', context={'uid': uid})


class HandleFileUpload(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            data = request.data

            serializer = FileListSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({
                    'status': 200,
                    'message': 'Files uploaded successfully',
                    'data': serializer.data
                })

            return Response({
                'status': 400,
                'message': 'something went wrong',
                'data': serializer.errors
            })
        except Exception as e:
            print(e)

