from django.http import JsonResponse
from django.views import View
import json
from decimal import Decimal

from core.services.frankfurter import FrankfurterService
from core.decorators import api_login_required
from core.forms import ConversionForm
from core.models import ConversionHistory,Watchlist

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from django.db import IntegrityError



class GetRatesView(View):

	@method_decorator(api_login_required)
	def get(self,request):
		base = request.GET.get('base','USD')
		symbols = request.GET.get('symbols')
		data = FrankfurterService.get_latest_rates(base,symbols)
		return JsonResponse(data)


class ConvertView(View):


	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	@method_decorator(api_login_required)	
	def post(self,request):
		try:
			data = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({"success":False,"error":"An error occurred while processing the data"},status=401)


		form = ConversionForm(data)

		if(form.is_valid()):
			from_currency = form.cleaned_data.get('from_currency')
			to_currency = form.cleaned_data.get('to_currency')
			amount = form.cleaned_data.get('amount')


			amount_data = FrankfurterService.get_latest_rates(from_currency,to_currency)
			try:
				rate = Decimal(str(amount_data['rates'][to_currency]))
			except (KeyError,TypeError):
				return JsonResponse({"success": False, "error": "Unsupported currency"}, status=400)
			calc = rate*amount

			date = amount_data['date']

			ConversionHistory.objects.create(
			    user=request.user,
			    from_currency=from_currency,
			    to_currency=to_currency,
			    amount=amount,
			    converted_amount=calc,
			    rate=rate,
			    converted_at=date
			)

			return JsonResponse({
			    "from": from_currency,
			    "to": to_currency,
			    "amount": float(amount),
			    "converted_amount": float(calc),
			    "rate": float(rate),
			    "date": date
			})
		else:
			return JsonResponse({"success":False, "errors": form.errors}, status=400)



class ConversionHistoryView(View):

	@method_decorator(api_login_required)
	def get(self,request):
		conversions = ConversionHistory.objects.filter(user=request.user).values('from_currency', 'to_currency', 'amount', 'converted_amount', 'rate', 'converted_at')
		return JsonResponse({"history": list(conversions)})
			

class SupportedCurrenciesView(View):

	def get(self,request):
		data = FrankfurterService.get_currencies()
		return JsonResponse({'currencies':data})


class WatchListView(View):


	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)



	@method_decorator(api_login_required)
	def get(self,request):
		watchlist = Watchlist.objects.filter(user=request.user).values('id', 'base_currency', 'target_currency', 'created_at')

		return JsonResponse({"watchlist": list(watchlist)})

	@method_decorator(api_login_required)
	def post(self,request):
		try:
			data = json.loads(request.body)
		except json.JSONDecodeError:
			return JsonResponse({"success":False,"error":"An error occurred while processing the data"},status=401)

		base_currency = data.get('base_currency')
		target_currency = data.get('target_currency')


		try:
			watchlist = Watchlist.objects.create(user=request.user,base_currency=base_currency,target_currency=target_currency)
			return JsonResponse({
				"id": watchlist.id,
				"base_currency": watchlist.base_currency,
				"target_currency":watchlist.target_currency,
			},status=201)
		except IntegrityError:
			return JsonResponse({"success": False, "error": "Already in watchlist"}, status=400)



class WatchListDeleteView(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)
		
	@method_decorator(api_login_required)
	def delete(self,request,pk):
		try:
			watchlist = Watchlist.objects.get(pk=pk,user=request.user)
			watchlist.delete()
			return JsonResponse({"success": True, "response": "Deleted"})
		except Watchlist.DoesNotExist:
			return JsonResponse({"success": False, "error": "Not found"}, status=404)