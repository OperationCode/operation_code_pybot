import logging

import pytest


from config.configs import configs
from ocbot.external.route_backend import OCBackend, ExpiredTokenException, InvalidTokenException, UndecodableTokenException

from tests.external_tests.test_route_backend_data import *
logger = logging.getLogger(__name__)

CORRECT_TOKEN = configs['BACK_JWT_TOKEN']
# NOT A REAL TOKEN DONT TRY BITCHES
BAD_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJzb21lIHJhbmRvbSBrZXkiLCJleHAiOjE4ODc1MjQ5Mzh9.cKikBK-AkMoIyAopLh1JjYi9cKyorkYE9FCX5LQHLy8'
SHORT_TOKEN = 'a'


# Good Health Check
def test_good_health():
    """
    Asserts build_message function correctly formats message.
    """
    client = OCBackend(jwt_token=CORRECT_TOKEN)
    resp = client.check_health()
    assert resp == True
    # assert resp.payload.message == good_health['payload']['message']
    # assert resp == good_health


def test_invalid_token(mocker):
    mocker.patch('ocbot.external.route_backend.OCBackend.req_get.response.json', return_value=incorrect_token)
    client = OCBackend(jwt_token=BAD_TOKEN)
    with pytest.raises(InvalidTokenException) as e_info:
        resp = client.check_health()


def test_expired_token(mocker):
    mocker.patch('ocbot.external.route_backend.OCBackend.req_get.response.json', return_value=expired_token)
    client = OCBackend(jwt_token=BAD_TOKEN)
    with pytest.raises(ExpiredTokenException) as e_info:
        resp = client.check_health()


def test_nondecodable_token(mocker):
    mocker.patch('ocbot.external.route_backend.OCBackend.req_get.response.json', return_value=non_decodeable_token)
    client = OCBackend(jwt_token=SHORT_TOKEN)
    with pytest.raises(UndecodableTokenException) as e_info:
        resp = client.check_health()
