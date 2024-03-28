from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from knox import views as knox_views

from . import views

app_name = 'users'
urlpatterns = [
    path('create', views.CreateUserViews.as_view(), name='create'),

    path('profile', views.ManageUserView.as_view(), name='profile'),

    path('login', views.LoginView.as_view(), name='knox-login'),
    path('logout', knox_views.LogoutView.as_view(), name='knox-logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(),
         name='knox-logoutall')
]

urlpatterns = format_suffix_patterns(urlpatterns)
