from django.urls import path
from django.contrib.auth import views as auth_views
from healthtrack import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_measurement, name='add_measurement'),
    path('export/', views.export_csv, name='export_csv'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
]
