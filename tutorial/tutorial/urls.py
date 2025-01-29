"""
URL configuration for tutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from tutorial import view
from tutorial.view import HomePageView, AboutPageView, CarreraCreateViewPage, CarreraEditarViewPage

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', view.index, name='index'),
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('carrera/', CarreraCreateViewPage.as_view(), name='carrera'),
    path('carrera/editar/<int:pk>/', CarreraEditarViewPage.as_view(), name='editar_carrera'),
]
