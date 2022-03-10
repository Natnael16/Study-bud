
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Message, Room, Topic
from .forms import RoomForm

from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout


def home(request):
    q = request.GET.get("q") if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    # print(room_count)
    all_messages = Message.objects.filter(Q(room__name__icontains = q))
    context = {'rooms' : rooms,'topics' : topics,'room_count':room_count,"all_messages": all_messages}
    return render(request,'base/home.html',context)


def room(request, pk):
    cur_room = Room.objects.get(id=pk)
    room_messages = cur_room.message_set.all().order_by('-created')
    participants = cur_room.participants.all()
    if request.method == 'POST':
        # body = request.POST.get('body')
        message = Message.objects.create(
            user = request.user,
            room = cur_room,
            body = request.POST.get('body')
        )
        cur_room.participants.add(request.user)
        return redirect('/room/{}'.format(pk))
    
            
    context = {'room':cur_room,'room_messages':room_messages,'participants': participants}
    return render(request,'base/room.html',context)

    
@login_required(login_url='/login')
def create_room(request):
    room = RoomForm()
    if request.method == 'POST':
        room = RoomForm(request.POST) 
        if room.is_valid:
            room.save()
            return redirect('home')
    context = {'form': room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='/login')
def update_room(request,pk):
    cur_room = Room.objects.get(id = pk)
    room = RoomForm(instance=cur_room)
    if request.user != cur_room.host:
        return HttpResponse("You Can Not Edit Another User's Post")
    if request.method == 'POST':
        room = RoomForm(request.POST, instance=cur_room) 
        if room.is_valid():
            room.save()
            return redirect('home')
    context= {'form': room}
    return render(request,'base/room_form.html',context)


@login_required(login_url='/login')
def delete_room(request,pk):
    room = Room.objects.get(id = pk)
    if request.user != room.host:
        return HttpResponse("You Can Not Edit Another User's Post")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})


def login_page(request):
    

    if request.user.is_authenticated:
        return redirect('home')


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        try:
            user = User.objects.get(username=username)
            print(username)
        except:
            messages.error(request,'Username Does not Exist!')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exist!')
    page = 'login'
    context = {'page':page}
    return render(request,'base/login_form.html',context)

def registerUser(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user  = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Registration requirments not fulfilled!')


    return render(request,'base/login_form.html', {'form':form})


def logout_page(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login')
def delete_message(request,pk):
    message = Message.objects.get(id = pk)
    if request.user != message.user:
        return HttpResponse("You are not allowed to delete anothor persons message!")
    if request.method == "POST":
        message.delete()
        return redirect('/room/{}'.format(str(message.room.id)))
    return render(request,"base/delete.html",{"obj":message})












