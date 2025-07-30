from django.contrib import admin
from django.urls import path, include
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('accounts.urls')),
]