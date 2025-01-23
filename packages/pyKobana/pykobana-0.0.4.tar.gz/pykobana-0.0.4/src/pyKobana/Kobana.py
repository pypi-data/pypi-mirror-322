import requests


class Kobana:
    url = ""
    __url_prod = "https://api.kobana.com.br/v1"
    __url_dev = "https://api-sandbox.kobana.com.br/v1"
    __api_token = ""

    def __init__(self, env, api_token):

        if env == "production":
            self.url = self.__url_prod
        else:
            self.url = self.__url_dev

        self.__api_token = api_token

    def doRequest(self, method, path, data=None, params=None):
        headers = {
            "Authorization": "Bearer " + self.__api_token,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        response = requests.request(method, self.url + path, headers=headers, data=data, params=params)
        return response.json()

    def doPost(self, path, data=None, params=None):
        return self.doRequest("POST", path, data, params)

    def doGet(self, path, data=None, params=None):
        return self.doRequest("GET", path, data=data, params=params)

    def doGetByParams(self, path, params=None):
        return self.doRequest("GET", path, data=None, params=params)

    def doPut(self, path, data=None, params=None):
        return self.doRequest("PUT", path, data)

    def doPatch(self, path, data=None, params=None):
        return self.doRequest("PATCH", path, data)

    def doDelete(self, path, data=None, params=None):
        return self.doRequest("DELETE", path, None)

    def getWallets(self, data=None, params=None):
        return self.doGet("/wallets")

    def getWalletById(self, id):
        return self.doGet("/wallets/" + id)

    def getWalletByExternalId(self, external_id):
        return self.doGet("/wallets/external/" + external_id)

    def getBankBillById(self, id):
        return self.doGet("/bank-bills/" + id)

    def getBankBillByExternalId(self, external_id):
        return self.doGet("/bank-bills/external/" + external_id)

    def findBankBill(self, params):
        return self.doGetByParams("/bank-bills", params)
