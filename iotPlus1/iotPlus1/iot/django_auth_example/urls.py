"""django_auth_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from users import views

urlpatterns = [
    url(r'^data', views.data,name='data'),
    url(r'^admin/', admin.site.urls),
    # 别忘记在顶部引入 include 函数
    url(r'^users/', include('users.urls')),
    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^$', views.user, name='user'),
    url(r'^index', views.index, name='index'),
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
    url(r'^list_shebei', views.list_shebei, name='list_shebei'),
    url(r'^delete_shebei', views.delete_shebei, name='delete_shebei'),
    url(r'^edit_shebei', views.edit_shebei, name='edit_shebei'),
]
