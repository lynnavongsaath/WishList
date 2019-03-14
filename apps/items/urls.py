from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.create, name="create"),
    url(r'^add_wish/$', views.add_wish, name="add_wish"),
    url(r'^delete_wish/$', views.delete_wish, name="delete_wish"),
    url(r'^remove_wish/$', views.remove_wish, name="remove_wish")
]