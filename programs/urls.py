from django.urls import path
from . import views

urlpatterns = [
    path('programs/', views.program_list, name='programs'),
    path('programs/<slug:slug>/', views.program_detail, name='program_detail'),
    path('scholarships/', views.scholarship_list, name='scholarships'),
    path('resources/', views.resource_list, name='resources'),
    path('resources/download/<int:pk>/', views.download_resource, name='download_resource'),
]
