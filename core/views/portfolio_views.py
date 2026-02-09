from django.http import JsonResponse
from django.views import View
import json

from core.services.frankfurter import FrankfurterService
from core.decorators import api_login_required
from core.models import Portfolio
from core.forms import PortfolioForm

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class PortfolioListCreateView(View):


	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)



	@method_decorator(api_login_required)
	def get(self,request):
		portfolio = Portfolio.objects.filter(user=request.user).values('id','currency_code','amount','purchase_rate','notes')
		return JsonResponse({"portfolio list":list(portfolio)})

	@method_decorator(api_login_required)
	def post(self,request):
		try:
			data = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({"success":False,"error":"An error occurred while processing the data"},status=401)

		form = PortfolioForm(data)
		if(form.is_valid()):
			currency_code = form.cleaned_data.get('currency_code')
			amount = form.cleaned_data.get('amount')
			purchase_rate = form.cleaned_data.get('purchase_rate')
			notes = form.cleaned_data.get('notes')
			portfolio = Portfolio.objects.create(
				user=request.user,
				currency_code=currency_code,
				amount=amount,
				purchase_rate=purchase_rate,
				notes=notes,
			)
			return JsonResponse({
			    "id": portfolio.id,
			    "currency_code": portfolio.currency_code,
			    "amount": float(portfolio.amount),
			    "purchase_rate": float(portfolio.purchase_rate),
			    "notes": portfolio.notes,
			    "created_at": str(portfolio.created_at)
			}, status=201)

		else:
			return JsonResponse({"success":False, "errors": form.errors}, status=400)


class PortfolioDetailView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	@method_decorator(api_login_required)
	def get(self,request,pk):
	    try:
	        portfolio = Portfolio.objects.get(pk=pk, user=request.user)
	        return JsonResponse({
	            "id": portfolio.id,
	            "currency_code": portfolio.currency_code,
	            "amount": float(portfolio.amount),
	            "purchase_rate": float(portfolio.purchase_rate),
	            "notes": portfolio.notes,
	            "created_at": str(portfolio.created_at)
	        })
	    except Portfolio.DoesNotExist:
	        return JsonResponse({"success": False, "error": "Not found"},status=404)

	@method_decorator(api_login_required)
	def put(self,request,pk):
		try:
			data = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({"success":False,"error":"An error occurred while processing the data"},status=401)

		form = PortfolioForm(data)
		if(form.is_valid()):
			currency_code = form.cleaned_data.get('currency_code')
			amount = form.cleaned_data.get('amount')
			purchase_rate = form.cleaned_data.get('purchase_rate')
			notes = form.cleaned_data.get('notes')

			try:
				portfolio = Portfolio.objects.get(pk=pk, user=request.user)
			except Portfolio.DoesNotExist:
				return JsonResponse({"success": False, "error": "Not found"}, status=404)

			portfolio.currency_code=currency_code
			portfolio.amount=amount
			portfolio.purchase_rate=purchase_rate
			portfolio.notes=notes

			return JsonResponse({
	            "id": portfolio.id,
	            "currency_code": portfolio.currency_code,
	            "amount": float(portfolio.amount),
	            "purchase_rate": float(portfolio.purchase_rate),
	            "notes": portfolio.notes
	        })

		else:
			return JsonResponse({"success":False, "errors": form.errors}, status=400)

	@method_decorator(api_login_required)
	def delete(self,request,pk):
		try:
			portfolio = Portfolio.objects.get(pk=pk, user=request.user)
		except Portfolio.DoesNotExist:
			return JsonResponse({"success": False, "error": "Not found"}, status=404)
		portfolio.delete()
		return JsonResponse({"success": True, "response": "Deleted"})


class SummaryView(View):

	@method_decorator(api_login_required)
	def get(self,request):
		portfolio = Portfolio.objects.filter(user=request.user)
		preferred = request.user.profile.preferred_currency

		array = []
		count = 0
		for i in portfolio:
			data = FrankfurterService.get_latest_rates(i.currency_code, preferred)
			current_rate = data['rates'][preferred]
			value = float(i.amount)*current_rate
			array.append({
                "currency_code": i.currency_code,
                "amount": float(i.amount),
                "current_rate": current_rate,
                "value_in_base": round(value,2)
             })
			count+=value

		return JsonResponse({
		    "total_value": round(count,2),
		    "currency": preferred,
		    "items": array
		})


