from django.conf.urls import include, url
import views

urlpatterns = [
    url(r'login',views.login),
    url(r'', views.index),
]