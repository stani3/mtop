"""mtop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mtop_app.urls')),
    path('', include('payments_app.urls')),
    path('register/', user_views.signup, name='register-home'),
    path('register/<str:ref_code>', user_views.affil, name='register-afil'),
    path('login/', user_views.loginPage, name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/affiliate', user_views.affiliate, name='affiliate'),
    path('profile/statistics', user_views.statistics, name='statistics'),
    path('profile/withdraw', user_views.withdraw, name='withdraw'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mtop-home'), name='logout'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
