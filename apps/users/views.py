from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from ..items.models import Item

def index(req):
    if 'user_id' not in req.session:
        return redirect('users:new')

    context = {
        'curr_user': User.objects.get(id=req.session['user_id']),
        'your_wish_list': Item.objects.filter(user_wished=req.session['user_id']),
        'others_wish_list': Item.objects.exclude(user_wished=req.session['user_id']),
    }
    return render(req,'users/index.html', context)

def show(req, id):
    if 'user_id' not in req.session:
        return redirect('users:new')

    try:
        item = Item.objects.get(id=id)
    except:
        return redirect('users:index')

    context = {
        'items': item,
        'users_wish': item.user_wished.all()
    }

    return render(req, 'users/show.html', context)

def new(req):
    return render(req, 'users/new.html')

def create(req):
    if req.method != 'POST':
        return redirect('users:new')

    # messages.add_message(request, LOGINERROR, '')
    errors = User.objects.validate(req.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(req, error)
    else:
        user = User.objects.create_user(req.POST)
        req.session['user_id'] = user.id
        req.session['name'] = user.name
        return redirect('users:index')

    return redirect('users:new')

def login(req):
    if req.method != 'POST':
        return redirect('users:new')

    valid, response = User.objects.login(req.POST)
    if valid == True:
        req.session['user_id'] = response
        return redirect('users:index')
    else:
        messages.error(req, response)
    return redirect('users:new')

def logout(req):
    req.session.clear()
    return redirect('users:new')

def add_item(req):
    if 'user_id' not in req.session:
        return redirect('users:new')
    return render(req, 'users/add.html')
