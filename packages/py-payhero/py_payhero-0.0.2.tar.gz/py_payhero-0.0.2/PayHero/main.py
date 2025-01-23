import requests
import base64
import json

class API():
    def __init__(self, api_username:str , api_password:str):
        credentials = f"{api_username}:{api_password}"
        credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        self.auth_token = f"Basic {credentials}"

    def get_service_balance(self):
        """
        Queries the service account wallet balance.
        """
        try:
            url ="https://backend.payhero.co.ke/api/v2/wallets?wallet_type=service_wallet"
            headers ={ "Authorization": self.auth_token}
            response= requests.get(url, headers=headers)
            if response.status_code ==200:
                return response.json()
        except Exception as error:
            print(error)

    def get_payment_balance(self):
        """
        Queries the payment wallet balance.
        """
        url = 'https://backend.payhero.co.ke/api/v2/wallets?wallet_type=payment_wallet'
        headers ={ "Authorization": self.auth_token}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as error:
            print(error)
        

    def topup_service_wallet(self, phone_number, amount: int):
        """
        Initiates a top-up for the service wallet on Pay Hero.
        """
        url = 'https://backend.payhero.co.ke/api/v2/topup'
        headers ={ "Authorization": self.auth_token}
        data ={
            "amount": amount,
            "phone_number":phone_number
        }
        try:
            response = requests.post(url, headers=headers, data= json.dumps(data) )
            if response.status_code ==201:
                return response.json()
            else:
                print( response.json() )
        except Exception as error:
            print(error)
        

    def initiate_mpesa_stk_push(self, amount:int , phone_number:str, channel_id:str, provider:str, external_reference:str, customer_name:str, callback_url:str):
        """
        Initiates an MPESA STK Push request to a customer's phone.
        """
        url = 'https://backend.payhero.co.ke/api/v2/payments'
        headers = {
            'Content-Type': 'application/json',
            "Authorization": self.auth_token
        }
        data = {
            "amount": amount,
            "phone_number": phone_number,
            "channel_id": channel_id,
            "provider": provider,
            "external_reference": external_reference,
            "customer_name": customer_name,
            "callback_url": callback_url
        }
        try:
            response = requests.post(url , headers=headers, data=json.dumps(data) )
            if response.status_code == 201:
                return response.json()
        except Exception as error:
            print(error)


    def fetch_transactions(self,page:int , per:int ):
        """
        Fetches the account transactions.

        """
        url = f'https://backend.payhero.co.ke/api/v2/transactions?page={page}&per={per}'
        headers ={ "Authorization": self.auth_token}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as error:
            print(error)
    
    def fetch_transaction_status(self, reference:str):
        """
        Fetches the account transactions.
        """
        url = 'https://backend.payhero.co.ke/api/v2/transaction-status?reference={reference}'
        headers ={ "Authorization": self.auth_token}
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
        except Exception as error:
            print(error)



    
