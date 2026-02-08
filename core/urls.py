from .views import auth_views
from django.urls import path


urlpatterns = [
	path('',auth_views.index,name='')

]