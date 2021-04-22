__author__ = 'nahla.errakik'

import requests
from http import HTTPStatus


class CovidAPI:
    def __init__(self):
        self._server = ' http://corona-api.com'

    def get_data(self):
        url = '{server}/countries'.format(server=self._server)
        response = requests.get(url)
        if response.status_code != HTTPStatus.OK:
            raise Exception('Error while calling external service')

        response = response.json()['data']
        return response





