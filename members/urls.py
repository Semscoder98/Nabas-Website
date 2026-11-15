from django.urls import path
from . import views

urlpatterns = [
    path('chapters/', views.chapters, name='chapters'),
    path('register/', views.register, name='register'),
    path('api/register/', views.register_api, name='register_api'),
    path('verify/<str:id_number>/', views.verify_member, name='verify_member'),
]
