from django.utils.crypto import get_random_string
import json, requests


class Card():

	def __init__(self,**kwargs):
		self.dicc = {}
		self.tokenAcept = ""
		self.token = "pub_test_Zs0LVNeaLOG440kKSAp0YRXBO8M0VBP0"
		self.tokePrivado = "prv_test_FVhEpj5NOK7JLMcP2aMqVDcHD5LNUwA8"
		self.idTarjeta = ""
		self.idFormaPago = ""
		self.idTransferecia = ""
		for key, value in kwargs.items():
			self.dicc[key] = value


	def envio(self,data,direccion,token,method):
		url = direccion
		data_string = json.dumps(data)
		payload = data_string
		headers = {
		    'Content-Type': 'application/json',
		    'Accept': 'application/json',
		    'Authorization': 'Bearer '+str(self.token)
		}
		if len(data) > 0:
			response = requests.request(method, url, headers=headers, data=payload,allow_redirects = False)
			response_dict = json.loads(response.text)
		else:
			response = requests.request(method, url, headers=headers,allow_redirects = False)
			response_dict = json.loads(response.text)
			self.tokenAcept = response_dict['data']['presigned_acceptance']['acceptance_token']

	def tokenAceptacion(self):
		data = {}
		url = "https://sandbox.wompi.co/v1/merchants/pub_test_Zs0LVNeaLOG440kKSAp0YRXBO8M0VBP0"
		
		self.envio(data,url,self.token,"GET")
		if int(self.validaTarjeta()) == 0:
			return 'Tarjeta Invalida'
		self.fuenteDePago()
		self.transaccion()
		return self.comprobarEstado()

	def validaTarjeta(self):
		data = {
		  "number": self.dicc['number'],
		  "exp_month": self.dicc['exp_month'],
		  "exp_year": self.dicc['exp_year'],
		  "cvc": self.dicc['cvc'],
		  "card_holder": self.dicc['card_holder']
		}
		url = "https://sandbox.wompi.co/v1/tokens/cards"
		method = 'POST'
		data_string = json.dumps(data)
		payload = data_string
		headers = {
		    'Content-Type': 'application/json',
		    'Accept': 'application/json',
		    'Authorization': 'Bearer '+str(self.token)
		}
		response = requests.request(method, url, headers=headers, data=payload,allow_redirects = False)
		response_dict = json.loads(response.text)
		print(response_dict)
		try:
			if str(response_dict['error']['messages']['number']).replace("['",'').replace("']",'') == "El número de tarjeta es inválido. Luhn check falló.":
				return 0
		except KeyError:
			self.idTarjeta = response_dict['data']['id']
			return 1
			

	def fuenteDePago(self):
		data = {
		  "type": "CARD",
		  "token": self.idTarjeta,
		  "customer_email": "pepito_perez@example.com",
		  "acceptance_token": self.tokenAcept
		}
		url = "https://sandbox.wompi.co/v1/payment_sources"
		method = 'POST'
		data_string = json.dumps(data)
		payload = data_string
		headers = {
		    'Content-Type': 'application/json',
		    'Accept': 'application/json',
		    'Authorization': 'Bearer '+str(self.tokePrivado)
		}
		response = requests.request(method, url, headers=headers, data=payload,allow_redirects = False)
		response_dict = json.loads(response.text)
		self.idFormaPago = response_dict["data"]["id"]

	def transaccion(self):
		token = get_random_string(length=19)
		data = {
		  "amount_in_cents": int(self.dicc['monto'].replace('.','')),
		  "currency": "COP",
		  "customer_email": "example@gmail.com",
		  "payment_method": {
		    "installments": 2
		  },
		  "reference":str(token),
		  "payment_source_id": self.idFormaPago
		}
		url = "https://sandbox.wompi.co/v1/transactions"
		method = 'POST'
		data_string = json.dumps(data)
		payload = data_string
		headers = {
		    'Content-Type': 'application/json',
		    'Accept': 'application/json',
		    'Authorization': 'Bearer '+str(self.tokePrivado)
		}
		response = requests.request(method, url, headers=headers, data=payload,allow_redirects = False)
		response_dict = json.loads(response.text)
		self.idTransferecia = response_dict['data']['id']

	def comprobarEstado(self):
		headers = {
		    'Content-Type': 'application/json',
		    'Accept': 'application/json',
		    'Authorization': 'Bearer '+str(self.token)
		}
		method = 'GET'
		url = "https://sandbox.wompi.co/v1/transactions/"+str(self.idTransferecia)
		response = requests.request(method, url, headers=headers,allow_redirects = False)
		response_dict = json.loads(response.text)
		return response_dict['data']['status']

		



