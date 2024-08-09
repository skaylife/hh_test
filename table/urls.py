from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('data_api/', views.data_api, name='data_api'),
    path('data_api2/', views.data_api2, name='data_api2'),
    path('admin/login/', views.CustomAdminLoginView.as_view(), name='admin_login'),
]
