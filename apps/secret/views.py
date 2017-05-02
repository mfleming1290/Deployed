from django.shortcuts import render, redirect, reverse
from django.db.models import F, Count, Value

from .models import Secret, User
# Create your views here.
def index(request):
    context = {
    'secrets': Secret.objects.all().order_by('-created_at')[:10],
    'user': User.objects.get(id=request.session['id']),
    'status': 'main'
    }
    return render(request, 'secret/index.html', context)


def post(request):
    if request.method == 'POST':
        valid, data = Secret.objects.post(request.POST, request.session['id'])
        if valid:
            return redirect(reverse('secret:index'))
        else:
            for err in data:
                messages.error(request, err)
            return redirect(reverse('secret:index'))

def like(request, sec_id):
    liked = Secret.objects.like(request, sec_id)
    return redirect('secret:index')

def popular(request):
    context = {
    'secrets': Secret.objects.annotate(num_all_likes=Count('liked_by')).order_by('-num_all_likes'),
    'user': User.objects.get(id=request.session['id']),
    'status': 'popular'
    }
    return render(request, 'secret/index.html', context)

def delete(request, mess_id):
    print "wtf"
    delete = Secret.objects.delete(request, mess_id)
    return redirect('secret:index')
