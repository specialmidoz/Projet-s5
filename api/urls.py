from django.conf.urls import include, url
import views


urlpatterns = [
    url(r'search',views.search),
    url(r'recommended',views.recommendVoituresUser)
]