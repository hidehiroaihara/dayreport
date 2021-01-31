"""dayreport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# 画像を扱い際に必要
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth.views import logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('report/',include('report.urls')),
    path('diary/',include('diary.urls')),
    # url(r'^logout/$', logout, {'template_name': 'index.html'}, name='logout'), 
    # path('accounts/',include('django.contrib.auth.urls')) #ログイン機能のパス
]

#画像を扱う前に必要
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)