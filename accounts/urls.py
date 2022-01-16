from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from vacancies import views
from accounts.views import UserSignupView, UserLoginView


app_name = 'accounts'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', UserSignupView.as_view(), name='signup'),
]
