from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data', views.data, name='data'),
    path('com', views.communicate, name='communicate'),
    path('detail',views.detail_page,name='detail'),
    path('login',views.login_page,name='login'),
    path('register', views.register_page, name='register'),
]