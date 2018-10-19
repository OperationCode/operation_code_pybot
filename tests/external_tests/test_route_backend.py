import logging

import pytest
import pytest_mock

from config.all_config_loader import configs
from ocbot.external.route_backend import OCBackend, ExpiredTokenException, InvalidTokenException, \
    UndecodableTokenException
from tests.external_tests.test_route_backend_data import *

logger = logging.getLogger(__name__)

CORRECT_TOKEN = configs['OC_BACKEND_JWT_TOKEN']
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
    mock = mocker.Mock
    mock.ok = False
    mock.json = lambda: invalid_token
    mock.status_code = 400
    mocker.patch('requests.get', return_value=mock)
    client = OCBackend(jwt_token=BAD_TOKEN)
    with pytest.raises(InvalidTokenException) as e_info:
        resp = client.check_health()




def test_expired_token(mocker):
    mock = mocker.Mock
    mock.ok = False
    mock.json = lambda: expired_token
    mock.status_code = 400
    mocker.patch('requests.get', return_value=mock)
    client = OCBackend(jwt_token=BAD_TOKEN)
    with pytest.raises(ExpiredTokenException) as e_info:
        resp = client.check_health()



def test_nondecodable_token(mocker):
    mock = mocker.Mock
    mock.ok = False
    mock.json = lambda: non_decodeable_token
    mock.status_code = 400
    mocker.patch('requests.get', return_value=mock)
    client = OCBackend(jwt_token=SHORT_TOKEN)
    with pytest.raises(UndecodableTokenException) as e_info:
        resp = client.check_health()
