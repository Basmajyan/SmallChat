from django.shortcuts import redirect, render
from . forms import UserRegister, UserLogin 
from django.contrib.auth import login as auth_login, logout as logoutuser
from django.contrib import messages
from django.shortcuts import render, redirect
from . models import Room, Message
from django.views.generic.list import ListView
from django.http import HttpResponse, JsonResponse

class HomeView(ListView):
    model = Room
    template_name = 'index.html'
    context_object_name = 'rooms'


def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,

    })


def checkview(request):
    room = request.POST['room_name']
    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/')
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/')


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})
    


def register(request):
    if request.method == "POST":
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request, 'Registration error')
    else:
        form = UserRegister()
        messages.error(request, 'Registration error')

    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserLogin()
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login.html', {'form': form, })


def logout(request):
    logoutuser(request)
    return redirect('/login')
