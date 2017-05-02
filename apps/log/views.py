from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User
# Create your views here.
def index(request):
    context = {
        'log': 'log'
    }
    return render(request, 'log/index.html', context)

def start_log(request):
    return redirect(reverse('log:index'))

def start_reg(request):
    context = {
        'log': 'reg'
    }
    return render(request, 'log/index.html', context)
def reg(request):
    if request.method == 'POST':
        valid, data = User.objects.register(request.POST)
        if valid:
            context = {
            'status': "registered"
            }
            request.session['name'] = request.POST['first_name']
            return render(request, 'log/success.html', context)
        else:
            for err in data:
                messages.error(request, err)
            return redirect(reverse('log:start_reg'))

def login(request):
    if request.method == 'POST':
        valid, data = User.objects.login(request.POST)
        if valid:

            user_info = User.objects.login(request.POST)
            context = {
            'first_name': user_info[1].first_name,
            'last_name': user_info[1].last_name,
            'email': user_info[1].email,
            'status': "logged in",
            'id': user_info[1].id
            }
            request.session['id'] = user_info[1].id
            request.session['name'] = user_info[1].first_name
            return render(request, 'log/success.html', context)
        else:
            for err in data:
                messages.error(request, err)
            return redirect(reverse('log:index'))

def user_info(request, id):
    if 'id' in request.session:

        user_info = User.objects.get(id=request.session['id'])
        id = request.session['id']
        context = {
        'first_name': user_info.first_name,
        'last_name': user_info.last_name,
        'email': user_info.email,
        'status': "logged in",
        'id': user_info.id
        }
        return render(request, 'log/user_info.html', context)
    else:
        return redirect(reverse('log:index'))

def delete_user(request):
    if request.method == 'POST':
        id = request.session['id']
        data = User.objects.delete_user(id)
        if data:
            print "deleted user"
            return redirect(reverse('log:index'))
        else:
            print "didnt work!"
            return redirect(reverse('log:index'))

def update_user(request):
    if request.method == 'POST':
        ids = request.session['id']
        valid, data = User.objects.update_user(ids, request.POST)
        if valid:
            messages.success(request, 'Profile details updated. Please log in again')
            return redirect(reverse('log:index'))
        else:

            for err in data:
                messages.error(request, err)

            user = User.objects.get(id=ids)
            context = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'status': "logged in",
            }
            print "didnt work!"
            return render(request, 'log/success.html', context)
def logout(request):
    request.session.clear()
    return redirect(reverse('log:index'))
