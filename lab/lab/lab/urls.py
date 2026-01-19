"""
URL configuration for lab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken.views import obtain_auth_token
from .views import DocsView

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/login/', obtain_auth_token),
    path('api/', include('user.urls')),
    # path('api/', include('post.urls')),
    path('api/', include('media.urls')),
    path('api/', include('plugin.urls')),
    # path('api/', include('comment.urls')),
    path('api/', include('theme.urls')),
    path("docs/", DocsView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
