from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    currency_code = models.CharField(max_length=3)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_rate = models.DecimalField(max_digits=15, decimal_places=6)
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Watchlist(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
	base_currency = models.CharField(max_length=3)
	target_currency = models.CharField(max_length=3)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		 unique_together = ["user", "base_currency", "target_currency"]


class ConversionHistory(models.Model):


	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversions')
	from_currency = models.CharField(max_length=3)
	to_currency = models.CharField(max_length=3)
	amount = models.DecimalField(max_digits=5, decimal_places=2)
	converted_amount = models.DecimalField(max_digits=5, decimal_places=2)
	rate = models.DecimalField(max_digits=15,decimal_places=6)
	converted_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-converted_at"]


class AIChat(models.Model):

	class TypeChoices(models.TextChoices):
		ADVICE = 'advice','Advice'
		ANALYSIS = 'analysis','Analysis'
		PORTFOLIO = 'portfolio','Portfolio'

	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_chats')
	question = models.TextField()
	answer = models.TextField()
	chat_type = models.CharField(max_length=20,choices=TypeChoices.choices)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]
			



