from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('needs/', views.needs_list, name='needs_list'),
    path('needs/<int:need_id>/', views.need_detail, name='need_detail'),
    path('problems/', views.problems_list, name='problems_list'),
    path('services/', views.services_list, name='services_list'),
    path('map/', views.map_view, name='map_view'),
    path('api/map-data/', views.map_data_api, name='map_data_api'),
    path('resources/', views.resources_list, name='resources_list'),
    path('resources/<int:resource_id>/', views.resource_detail, name='resource_detail'),
    path('disasters/', views.disasters_list, name='disasters_list'),
    path('disasters/<slug:disaster_slug>/', views.disaster_detail, name='disaster_detail'),
]
