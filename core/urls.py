from .views import auth_views
from django.urls import path


urlpatterns = [
	path('auth/register/',auth_views.RegisterView.as_view(),name='register_view'),
	path('auth/login/',auth_views.LoginView.as_view(),name='login_view'),
	path('auth/logout/',auth_views.LogoutView.as_view(),name='logout_view'),
	path('auth/profile/',auth_views.ProfileView.as_view(),name='profile_view')

]