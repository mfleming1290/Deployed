from django.conf.urls import url
from . import views

app_name = 'secret'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post$', views.post, name='post'),
    url(r'^like/(?P<sec_id>\d+)$', views.like, name='like'),
    url(r'^delete/(?P<mess_id>\d+)$', views.delete, name='delete'),
    url(r'^popular$', views.popular, name='popular'),

]
