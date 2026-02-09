from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.Form):
	username = forms.CharField(min_length=3,max_length=30)
	email = forms.EmailField()
	password = forms.CharField(min_length=8,max_length=12)
	password_confirm = forms.CharField(min_length=8,max_length=12)



	def clean_username(self):
		username = self.cleaned_data['username']
		if(User.objects.filter(username=username).exists()):
			raise forms.ValidationError("This user exists")

		return username

	def clean_email(self):
		email = self.cleaned_data['email']
		if(User.objects.filter(email=email).exists()):
			raise forms.ValidationError("This email exists")

		return email

	def clean(self):
		cleaned_data = super().clean()
		password = cleaned_data.get('password')
		password_confirm = cleaned_data.get('password_confirm')
		if(password and password_confirm and password!=password_confirm):
			raise forms.ValidationError('password dont match')
		return cleaned_data

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField()


class ConversionForm(forms.Form):
    from_currency = forms.CharField(max_length=3)
    to_currency = forms.CharField(max_length=3)
    amount = forms.DecimalField(min_value=0.01)