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
from tutorial.view import HomePageView, AboutPageView, CarreraCreateViewPage, CarreraEditarViewPage, AuthorCreateViewPage, AuthorDeleteViewPage, AuthorEditarViewPage, LibroCreateViewPage, LibroDeleteViewPage, LibroEditarViewPage, UserCreateViewPage, UserDeleteViewPage, UserEditarViewPage, PrestamoCreateViewPage, PrestamoDeleteViewPage, PrestamoEditarViewPage, CategoriaCreateViewPage, CategoriaDeleteViewPage, CategoriaEditarViewPage
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', view.index, name='index'),
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('carrera/', CarreraCreateViewPage.as_view(), name='carrera'),
    path('carrera/editar/<int:pk>/', CarreraEditarViewPage.as_view(), name='editar_carrera'),
    path('carrera/eliminar/<int:pk>/', view.CarreraDeleteViewPage.as_view(), name='eliminar_carrera'),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="login.html"), name='logout'),
    path('autor/', AuthorCreateViewPage.as_view(), name='autor'),
    path('autor/eliminar/<int:pk>/', AuthorDeleteViewPage.as_view(), name='eliminar_autor'),
    path('autor/editar/<int:pk>/', AuthorEditarViewPage.as_view(), name='editar_autor'),
    path('libro/', LibroCreateViewPage.as_view(), name='libro'),
    path('libro/eliminar/<int:pk>/', LibroDeleteViewPage.as_view(), name='eliminar_libro'),
    path('libro/editar/<int:pk>/', LibroEditarViewPage.as_view(), name='editar_libro'),
    path('usuario/', UserCreateViewPage.as_view(), name='usuario'),
    path('usuario/eliminar/<int:pk>/', UserDeleteViewPage.as_view(), name='eliminar_usuario'),
    path('usuario/editar/<int:pk>/', UserEditarViewPage.as_view(), name='editar_usuario'),
    path('prestamo/', PrestamoCreateViewPage.as_view(), name='prestamo'),
    path('prestamo/eliminar/<int:pk>/', PrestamoDeleteViewPage.as_view(), name='eliminar_prestamo'),
    path('prestamo/editar/<int:pk>/', PrestamoEditarViewPage.as_view(), name='editar_prestamo'),
    path('categoria/', CategoriaCreateViewPage.as_view(), name='categoria'),
    path('categoria/eliminar/<int:pk>/', CategoriaDeleteViewPage.as_view(), name='eliminar_categoria'),
    path('categoria/editar/<int:pk>/', CategoriaEditarViewPage.as_view(), name='editar_categoria'),
]
