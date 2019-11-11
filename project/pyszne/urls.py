from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^scraper/', views.scraper, name='scraper'),
    url(r'^$', views.index, name='index'),
    url(r'scraper/', views.scraper, name='scraper')
];

#
# from django.urls import path
# from django.conf import settings
#
# from . import views
#
# urlpatterns = [
#     path('pyszne', views.index, name='index'),
#     path('scraper', views.scraper, name='scraper'),
#     path('', views.index)
# ]