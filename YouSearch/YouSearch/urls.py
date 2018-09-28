"""YouSearch URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='index/')),

    path('admin/', admin.site.urls),

    path('index/', include('apps.index.urls')),

    path('upload/', include('apps.upload.urls')),

    path('login/', include('apps.login.urls')),

    path('analytics/', include('apps.analytics.urls', namespace='analytics'), name='analytics'),

    path('signup/', include('apps.signup.urls')),

    path('userprof/', include('apps.userprof.urls')),

    path('edit/', include('apps.edit.urls')),

    path('password/', include('apps.password.urls')),

    path('dashboard/', include('apps.dashboard.urls')),

    path('chart/', include('apps.chart.urls')),
    
    path('api/', include('apps.api.urls'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
