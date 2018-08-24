import requests


class DaDataGateway:
    token = '85d2b0a154c56a35265e5216660e6a0f98c3c9ec'
    base_url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/'

    def __init__(self, token: str = ''):
        if token:
            self.token = token

    def request(self, point: str, data: dict):
        headers = {
            'content-type': 'application/json',
            'accept': 'application/json',
            'authorization': 'Token {}'.format(self.token)
        }
        response = requests.post(url=self.base_url+point, json=data, headers=headers)
        return response.json()

    def address(self, query: str, count: int):
        return self.request(point='address', data={'query': query, 'count': count})['suggestions']
