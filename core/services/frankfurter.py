import requests

class FrankfurterService:

	url = 'https://api.frankfurter.dev/v1/'

	@staticmethod
	def get_latest_rates(base='USD',symbols=None):
		try:
			response = requests.get(FrankfurterService.url+'latest',params={'base': base, 'symbols': symbols})
			if(response.status_code==200):
				return response.json()
			else:
				return "Error"
		except requests.RequestException:
			return 'An error occurred while sending the request'

	@staticmethod
	def get_currencies():
		try:
			response = requests.get(FrankfurterService.url+'currencies')
			if(response.status_code==200):
				return response.json()
			else:
				return 'Error'
		except requests.RequestException:
			return 'An error occurred while sending the request'

	@staticmethod
	def get_historical(date,base='USD',symbols=None):
		try:
			response = requests.get(FrankfurterService.url+str(date),params={'base':base,'symbols':symbols})
			if(response.status_code==200):
				return response.json()
			else:
				return "Error"
		except requests.RequestException:
			return 'An error occurred while sending the request'


print(FrankfurterService.get_latest_rates('USD','EUR')['rates']['EUR'])