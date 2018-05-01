from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
import json

from rest_framework.decorators import api_view

from .serializers import QuestsSerializer
from .forms import Registerkey,Loginform,Postone,Deleteone,Updateone, Getlist, Getone, Forgotkey
from .models import user

import os



"""View to return home page"""
@api_view(['GET'])
def HomePage(request):
    return render(request, "index.html")


"""Returns django form to save user's credential"""
@api_view(['GET'])
def RegisterKey(request):
    form=Registerkey()
    return render(request,'register.html',{'form': form})

@api_view(['GET'])
def LoginForm(request):
    form=Loginform()
    return render(request,'login.html',{'form': form})


"""Returns django form to post one image on file system"""
@api_view(['GET'])
def PostOne(request):
    form = Postone()
    return render(request,'postone.html',{'form':form})


"""Returns django form to get all images associated with the provided access key"""
@api_view(['GET'])
def GetList(request):
    form=Getlist()
    return render(request, 'getlist.html', {'form': form})


"""Returns django form to get one image"""
@api_view(['GET'])
def GetOne(request):
    form=Getone()
    return render(request,'getone.html',{'form':form})


"""Returns django form to delete one image"""
@api_view(['GET'])
def DeleteOne(request):
    form=Deleteone()
    return render(request, 'deleteone.html', {'form': form})


"""Returns django form to update one image"""
@api_view(['GET'])
def UpdateOne(request):
    form=Updateone()
    return render(request, 'updateone.html', {'form': form})


"""Returns django form to handle forget key request"""
@api_view(['GET'])
def ForgotKey(request):
    form=Forgotkey()
    return render(request, 'forgotkey.html', {'form': form})


"""View to save users credential to db"""
@api_view(['POST'])
def Sign(request):
    #accepting parameters, converting data into json format and saving to the db
    name = request.POST['name']
    key = request.POST['key']
    email=request.POST['email']
    js = {'name': name, 'key': key,'email':email}
    serial = QuestsSerializer(data=js)
    if (serial.is_valid()):
        print(serial)
        serial.save()
        request.session['email']=email
        link = "http://34.203.210.28:8080/api/" + email + "/" + key
        return render(request,'index.html',{'name': name,'link':link})
    return Response(status=status.HTTP_400_BAD_REQUEST)


"""As per the instrunction of the api specs, list function handles thre request,
    GET   : dispaly all image,
    POST  : save one image
"""
@api_view(['GET','POST'])
def List(request):
    #dispaly all image
    if (request.method=='GET'):
        try:
            email=request.session['email']
            obj = user.objects.filter(email=email).values('name','key')
            key =obj[0]['key']
            print(obj)
            # framing folder name eg: (user's name)_(user's key)
            folder = "tmp/" + obj[0]['name'] + "_" + key
            dir_path = (folder)
            img_list = os.listdir(dir_path)
            folder=obj[0]['name'] + "_" + key
            arr = []
            brr = []
            #store location of the entire images inside directory dir_path
            for i in range(len(img_list)):
                arr.append(folder + "/" + img_list[i])

            print(arr)
            # return HttpResponse(arr, content_type='application/json')
            return render(request, 'display.html', {'arr': arr,'brr':img_list})
        except BaseException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    #save one image
    elif (request.method=='POST'):

        try:
            email=request.session['email'];
        except:
            form = Loginform()
            return render(request, 'login.html', {'form': form})

        img = request.FILES['image']
        img_name = img.name
        try:
            obj = user.objects.filter(email=email).values('name','key')
            folder = obj[0]['name'] + "_" + obj[0]['key']
            dir_path = ("tmp/" + folder)
        except BaseException as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            os.mkdir(dir_path)
        except OSError as e:
            print(e)
        f = open(dir_path + "/" + img_name, 'wb')
        for chunk in img.chunks():
            f.write(chunk)

        link="http://34.203.210.28:8080/api/"+email+"/"+obj[0]['key']
        return render(request, 'index.html', {'name': obj[0]['name'],'link':link})


"""Its a repeat function to delete an image via django forms
    used this function because i was not able to send DELETE request from form"""
@api_view(['POST'])
def Delete(request):
    img = request.POST['name']
    try:
        email = request.session['email']
        obj = user.objects.filter(email=email).values('name', 'key')
        key = obj[0]['key']
        folder = obj[0]['name'] + "_" + key
        dir_path = ("tmp/" + folder)
        img_list = os.listdir(dir_path)
        dir_path = dir_path + "/" + img
        print(dir_path, img_list, img, len(img_list))
        os.remove(dir_path)
    except BaseException as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    link = "http://34.203.210.28:8080/api/" + email + "/" + obj[0]['key']
    return render(request, 'index.html', {'name': obj[0]['name'],'link':link})


"""Its a repeat function to update an image via django forms
    used this function because i was not able to send PATCH request from form"""
@api_view(['POST'])
def Patch(request):
    img = request.FILES['image']
    img_name = img.name
    print(img_name)
    try:
        email = request.session['email']
        obj = user.objects.filter(email=email).values('name', 'key')
        key = obj[0]['key']

        folder = obj[0]['name'] + "_" + key
        dir_path = ("tmp/" + folder)
        img_list = os.listdir(dir_path)
        f = open(dir_path + "/" + img_name, 'wb')
    except BaseException as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    flag = 0
    for i in range(len(img_list)):
        if (img_list[i] == img_name):
            flag = 1
            break
    print(flag)
    if (flag == 0):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    for chunk in img.chunks():
        f.write(chunk)
    link = "http://34.203.210.28:8080/api/" + email + "/" + obj[0]['key']
    return render(request, 'index.html', {'name': obj[0]['name'],'link':link})


"""An end point to access key, This function sends the access key to the user's email address"""
@api_view(['POST'])
def MailKey(request):
    email=request.POST['email']
    print(email)
    try:
        obj = user.objects.filter(email=email)
        ema=obj[0].email
        key=obj[0].key
        send_mail(
            'Access Key',
            'your access key is '+key,
            settings.EMAIL_HOST_USER,
            [ema],
            fail_silently=True
        )

    except BaseException as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST','GET'])
def LogIn(request):

    #accepting parameters, converting data into json format and saving to the db
    try:
        if (request.session['email']!=None):
            email=request.session['email']
            obj = user.objects.filter(email=email).values('name','key')
            link = "http://34.203.210.28:8080/api/" + email + "/" + obj[0]['key']
            return render(request, 'index.html', {'name': obj[0]['name'],'link':link})
    except:
        print("No session")

    try:
        key = request.POST['key']
        email=request.POST['email']
        obj = user.objects.filter(email=email,key=key).values('name')
        print(len(obj))
        if (len(obj)==1):
            request.session['email'] = email
            link = "http://34.203.210.28:8080/api/" + email + "/" + key
            return render(request, 'index.html', {'name': obj[0]['name'],'link':link})
        else:
            form = Loginform()
            print("cdsafsadfas")
            return render(request, 'login.html', {'form': form})

    except:
        form = Loginform()
        print("Ohh no")
        return render(request, 'login.html', {'form': form})


@api_view(['POST','GET'])
def LogOut(request):
    # request.session.set_expiry(SESSION_COOKIE_AGE)
    del request.session['email']
    form = Loginform()
    return render(request, 'login.html', {'form': form})

@api_view(['GET'])
def Api(request,email,key):
    print(email,key)
    try:
        obj = user.objects.filter(email=email).values('name', 'key')
        # framing folder name eg: (user's name)_(user's key)
        if (key==obj[0]['key']):
            folder = "tmp/" + obj[0]['name'] + "_" + key
            dir_path = (folder)
            img_list = os.listdir(dir_path)
            folder = obj[0]['name'] + "_" + key
            arr = {}
            # store location of the entire images inside directory dir_path
            for i in range(len(img_list)):
                arr[str(i)]=str("http://34.203.210.28:8080/tmp/"+folder + "/" + img_list[i])

            data = json.dumps(arr)
            print (data)
            return HttpResponse(data,content_type='application/json')
            # return HttpResponse(arr, mimetype='application/json')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except BaseException as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

