import logging

import requests

from config.all_config_loader import configs

logger = logging.getLogger(__name__)
JWT_BACKEND_TOKEN = configs['OC_BACKEND_JWT_TOKEN']
OC_BACKEND_URL = configs['OC_BACKEND_URL']


class OCBackend:
    # Store the instance

    _back_suffix = 'api/v1/slack_users'
    _bearer_token = ''

    def __init__(self, *, jwt_token=None):
        self._verification_token = jwt_token or JWT_BACKEND_TOKEN
        self._bearer_token = f'Bearer {self._verification_token}'

    def build_url(self, route_string):
        return f'{OC_BACKEND_URL}/{self._back_suffix}/{route_string}'

    def check_health(self):
        route_url = self.build_url('access')

        response = self.do_get(route_url)

        if not response.ok:
            val = response.json()
            raise OCException(response.json()['errors'][0], response.status_code)

        return True

    def do_get(self, route_url):
        return requests.get(route_url, headers={"Authorization": self._bearer_token})


class OCException(Exception):
    def __init__(selfself, message, status_code):
        bad_response_dict = {'Invalid auth token': UndecodableTokenException,
                             'Auth token has expired': ExpiredTokenException,
                             'Auth token is invalid': InvalidTokenException,
                             }

        raise bad_response_dict[message]()


class ExpiredTokenException(OCException):
    def __init__(self):
        self.message = 'Expired Auth Token'


class InvalidTokenException(OCException):
    def __init__(self):
        self.message = 'Incorrect JWT token sent'


class UndecodableTokenException(OCException):
    def __init__(self):
        self.message = 'Server Couldn\'t decode token'
