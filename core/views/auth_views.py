from django.http import JsonResponse
from django.views import View
import json

from core.models import UserProfile
from core.forms import RegistrationForm,LoginForm
from core.decorators import api_login_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

class RegisterView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	def post(self,request):
		try:
			data = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({"success":False,"error":"An error occurred while processing the data"},status=401)

		form = RegistrationForm(data)
		if(form.is_valid()):
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']

			user = User.objects.create_user(username=username, email=email, password=password)
			UserProfile.objects.create(user=user)
			login(request,user)

			return JsonResponse({"success":True, "response":"User created"},status=201)
		else:
			return JsonResponse({"success":False, "errors": form.errors}, status=400)


class LoginView(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)


	def post(self,request):
		try:
			data = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({"success":False,"error":"An error occurred while processing the data"},status=401)

		form = LoginForm(data)
		if(form.is_valid()):
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = authenticate(request, username=username, password=password)
			if(user is not None):
			    login(request, user)
			    return JsonResponse({"success": True, "response": "login success"}, status=200)
			else:
			    return JsonResponse({"success": False, "error": "Invalid credentials"}, status=401)
		else:
			return JsonResponse({"success":False, "errors": form.errors}, status=400)


class LogoutView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	@method_decorator(api_login_required)
	def post(self,request):
		logout(request)
		return JsonResponse({"success": True, "response": "logout success"}, status=200)

class ProfileView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)


	@method_decorator(api_login_required)
	def get(self,request):
		user = request.user
		return JsonResponse({
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                'preferred_currency':user.profile.preferred_currency,
                'created_at':user.profile.created_at
            }
        })