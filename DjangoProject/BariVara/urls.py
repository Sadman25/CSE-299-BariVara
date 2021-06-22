
from django.contrib import admin
from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.HomePage, name='HomePage'),
    path('create_advertisements', views.create_advertisements, name='create_advertisements'),
    path('advertisement_edit/<int:id>/', views.advertisement_edit, name='advertisement_edit'),
    path('advertisement_delete/<int:id>/', views.advertisement_delete, name='advertisement_delete'),
    path('advertisement_details/<int:id>/', views.advertisement_details, name='advertisement_details'),
    path('search', views.Search, name='search'),
    path('filter', views.Filter, name='filter'),
    path('your_advertisements',views.your_advertisements, name='your_advertisements'),
    

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
