from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Item

def create(req):
    if req.method != 'POST':
        print("this is not via post")
        return redirect('users:new')
    
    errors = Item.objects.validate(req.POST)
    if len(errors) > 0:
        for error in errors:
            messages.error(req, error)
    else:
        Item.objects.create_item(req.POST)
        return redirect ('users:index')

    return redirect('users:add_item')

def add_wish(req):
    if req.method != 'POST':
        return redirect('users:new')
    else:
        Item.objects.add_wish(req.POST)
        return redirect('users:index')
   
    return redirect('users:new')

def remove_wish(req):
    if req.method != 'POST':
        return redirect('users:new')
    else:
        Item.objects.remove_wish(req.POST)
        return redirect('users:index')
    
    return redirect('users:new')

def delete_wish(req):
    if req.method != 'POST':
        return redirect('users:new')
    else:
        Item.objects.delete_wish(req.POST)
        return redirect('users:index')
        
    return redirect('users:new')