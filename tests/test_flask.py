#!flask/bin/python
import json
import logging

import pytest
import config.all_config_loader
import ocbot.web.routes_web
import ocbot.web.routes_slack
from tests import VALIDATE_RESPONSE_PATH, ROUTING_HANDLER_PATH, GOOD_TOKEN
from tests.handler_tests.action_menu_events import SUGGESTION_CLICKED_EVENT
from tests.test_data import CHALLENGE, NEW_MEMBER
from pytest_mock import mocker

logging.disable(logging.CRITICAL)


@pytest.fixture
def test_app():
    config.all_config_loader.configs['VERIFICATION_TOKEN'] = GOOD_TOKEN
    from ocbot import app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False
    return app.test_client()


# Request Verification Tests #
def test_good_slack_token(mocker: mocker, test_app):
    data = NEW_MEMBER
    data['token'] = GOOD_TOKEN
    json_data = json.dumps(data)
    mock = mocker.patch(ROUTING_HANDLER_PATH)
    response = test_app.post('/event_endpoint', data=json_data,
                             content_type='application/json',
                             follow_redirects=True)
    assert mock.called
    assert response.status_code == 200


def test_event_with_bad_slack_token(mocker, test_app):
    data = NEW_MEMBER
    data['token'] = 'bad token'
    json_data = json.dumps(data)
    mocker.patch(ROUTING_HANDLER_PATH)
    response = test_app.post('/event_endpoint', data=json_data,
                             content_type='application/json',
                             follow_redirects=True)
    assert not ocbot.web.routes_slack.RoutingHandler.called
    assert response.status_code == 403


def test_interaction_with_bad_slack_token(mocker, test_app):
    data = SUGGESTION_CLICKED_EVENT
    data['token'] = 'bad token'
    json_data = json.dumps(data)
    mocker.patch(ROUTING_HANDLER_PATH)
    response = test_app.post('/user_interaction', data=dict(payload=json_data),
                             follow_redirects=True)
    assert not ocbot.web.routes_slack.RoutingHandler.called
    assert response.status_code == 403


def test_empty_slack_value_token(mocker, test_app):
    data = NEW_MEMBER
    data['token'] = None
    json_data = json.dumps(data)
    mocker.patch(ROUTING_HANDLER_PATH)
    response = test_app.post('/event_endpoint', data=json_data,
                             content_type='application/json',
                             follow_redirects=True)
    assert not ocbot.web.routes_slack.RoutingHandler.called
    assert response.status_code == 403


def test_empty_token_slack_data(mocker, test_app):
    mocker.patch(ROUTING_HANDLER_PATH)
    response = test_app.post('/event_endpoint', data=None,
                             content_type='application/json',
                             follow_redirects=True)
    assert not ocbot.web.routes_slack.RoutingHandler.called
    assert response.status_code == 400


# Challenge verification tests #
def test_challenge_redirect(mocker, test_app):
    data = json.dumps(CHALLENGE)
    mocker.patch(ROUTING_HANDLER_PATH)
    response = test_app.post('/event_endpoint', data=data,
                             content_type='application/json',
                             follow_redirects=True)
    assert not ocbot.web.routes_slack.RoutingHandler.called
    assert response.status_code == 200


def test_url_verified_called(mocker, test_app):
    """
    :param mock: combined_route_director, don't want to call function
    :return:
    This case tests if we have a verification token
    """
    CHALLENGE['token'] = GOOD_TOKEN
    data = json.dumps(CHALLENGE)
    mocker.patch(ROUTING_HANDLER_PATH)
    mocker.patch(VALIDATE_RESPONSE_PATH)

    response = test_app.post('/event_endpoint', data=data,
                             content_type='application/json',
                             follow_redirects=True)

    assert not ocbot.web.routes_slack.RoutingHandler.called
    assert not ocbot.web.routes_slack.validate_response.called
    assert response.status_code == 200
