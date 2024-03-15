"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


from . import settings


from main.views import MainView, CategoryView, GoodView, add_to_cart, search

urlpatterns = [
    path('', MainView.as_view(), name="main"),
    path('category/<int:category_id>', CategoryView.as_view(), name="category"),
    path('good/<int:good_id>', GoodView.as_view(), name="good"),
    path('admin/', admin.site.urls),

    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/profile/", RedirectView.as_view(url="/")),


    path('api/add_to_cart/<int:good_id>', add_to_cart, name="add_to_cart"),
    path('api/search/<int:category_id>/<str:query>', search, name="search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
