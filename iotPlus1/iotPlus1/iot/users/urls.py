from django.conf.urls import url

from . import views

app_name = 'users'
urlpatterns = [
    url(r'^data', views.data,name='data'),
    url(r'^register/', views.register, name='register'),
    url(r'^index', views.index, name='index'),
    url(r'^user', views.user, name='user'),
    url(r'^pyecharts', views.pyecharts, name='pyecharts'),
    url(r'^design', views.design, name='design'),
    url(r'^water', views.water, name='water'),
    url(r'^detail', views.detail, name='detail'),
    url(r'^add', views.add, name='add'),
    url(r'^jiankong', views.jiankong, name='jiankong'),
    url(r'^charts1', views.charts1, name='pyecharts1'),
    url(r'^charts2', views.charts2, name='pyecharts2'),
    url(r'^charts3', views.charts3, name='pyecharts3'),
    url(r'^charts4', views.charts4, name='pyecharts4'),
    # url(r'^shebei', views.shebei, name='shebei'),

]
