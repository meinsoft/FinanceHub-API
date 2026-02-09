from .views import auth_views,currency_views
from django.urls import path


urlpatterns = [
	path('auth/register/',auth_views.RegisterView.as_view()),
	path('auth/login/',auth_views.LoginView.as_view()),
	path('auth/logout/',auth_views.LogoutView.as_view()),
	path('auth/profile/',auth_views.ProfileView.as_view()),

	path('currency/rates/',currency_views.GetRatesView.as_view()),
	path('currency/convert/',currency_views.ConvertView.as_view()),
	path('currency/history/',currency_views.ConversionHistoryView.as_view()),
	path('currency/currencies/',currency_views.SupportedCurrenciesView.as_view()),
	path('currency/watchlist/',currency_views.WatchListView.as_view()),
	path('currency/watchlist/<int:pk>/', currency_views.WatchListDeleteView.as_view())

]