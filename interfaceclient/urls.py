from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'interfaceclient',views.interfaceclient),
    url(r'registeruser',views.registeruser),
    url(r'loginuser',views.loginuser),
    url(r'vitrine', views.vitrine),

]