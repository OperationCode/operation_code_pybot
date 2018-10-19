import pytest
import pytest_mock
from ocbot.external.route_slack import Slack, SlackBuilder
from ocbot.external.route_airtable import AirTableBuilder
from config.all_config_loader import configs

from ocbot.pipeline.handlers.airtable_request_handler import NewAirtableRequestHandler
from tests.handler_tests.airtable_request_events import NEW_AIRTABLE_REQUEST_JSON, USER_ID_FROM_EMAIL_RESPONSE, \
    TEXT_DICT_MESSAGE, TEXT_DICT_DETAILS, MENTOR_REQUEST_ATTACHMENT, TEXT_DICT_MATCHES

RECORD_TO_SERVICE = 'ocbot.external.route_airtable.AirTableBuilder.record_to_service'
SLACK_AUTH_TEST = 'ocbot.external.route_slack.Slack.auth_test'
SLACK_GET_ID = 'ocbot.pipeline.handlers.airtable_request_handler.NewAirtableRequestHandler.check_user_id_cache'

MENTORS_INTERNAL_CHANNEL = configs['SLACK_MENTORS_INTERNAL_CHANNEL']
SLACK_USER_ID = '<@AGF2354>'


@pytest.fixture
def new_request_handler():
    handler = NewAirtableRequestHandler(event_dict=NEW_AIRTABLE_REQUEST_JSON)
    handler.api_dict['complete_matches'] = ''
    handler.api_dict['partial_matches'] = ''
    handler.text_dict['complete_matches'] = ''
    handler.text_dict['partial_matches'] = ''

    return handler


def test_email_pulled_from_request(new_request_handler: NewAirtableRequestHandler):
    assert new_request_handler._user_email == NEW_AIRTABLE_REQUEST_JSON['Email']


def test_event_dict_pulled_from_request(new_request_handler: NewAirtableRequestHandler):
    assert new_request_handler._event == NEW_AIRTABLE_REQUEST_JSON


def test_slack_queried_for_user_id_from_email(mocker: pytest_mock, new_request_handler: NewAirtableRequestHandler):
    mocker.patch(SLACK_AUTH_TEST, return_value=True)
    mocker.patch.object(Slack, "user_id_from_email", return_value=USER_ID_FROM_EMAIL_RESPONSE)
    new_request_handler.api_calls()
    assert new_request_handler.api_dict['user'] == SLACK_USER_ID


def test_event_slack_user_used_when_user_id_query_fails(mocker: pytest_mock,
                                                        new_request_handler: NewAirtableRequestHandler):
    mocker.patch(SLACK_AUTH_TEST, return_value=True)
    mocker.patch.object(Slack, "user_id_from_email", return_value={'ok': False})
    new_request_handler.api_calls()
    assert new_request_handler.api_dict['user'] == NEW_AIRTABLE_REQUEST_JSON['Slack User']


def test_airtable_builder_called_to_translate_service(mocker: pytest_mock,
                                                      new_request_handler: NewAirtableRequestHandler):
    airtable_mock = mocker.patch(RECORD_TO_SERVICE, return_value="fakerec")
    new_request_handler.api_dict['user'] = SLACK_USER_ID
    new_request_handler.api_dict['matches'] = SLACK_USER_ID

    new_request_handler.build_templates()

    assert airtable_mock.call_count == 1


def test_text_dict_populated(mocker: pytest_mock, new_request_handler: NewAirtableRequestHandler):
    airtable_mock = mocker.patch(RECORD_TO_SERVICE, return_value="fakerec")
    mocker.patch(SLACK_GET_ID, return_value=SLACK_USER_ID)
    new_request_handler.api_dict['matches'] = SLACK_USER_ID
    new_request_handler.api_dict['user'] = SLACK_USER_ID

    new_request_handler.build_templates()

    assert new_request_handler.text_dict['message']
    assert new_request_handler.text_dict['details']


def test_correct_response_added(mocker: pytest_mock, new_request_handler: NewAirtableRequestHandler):
    airtable_mock = mocker.patch(RECORD_TO_SERVICE, return_value="fakerec")
    mocker.patch(SLACK_GET_ID, return_value=SLACK_USER_ID)
    new_request_handler.text_dict['matches'] = TEXT_DICT_MATCHES
    new_request_handler.text_dict['message'] = TEXT_DICT_MESSAGE
    new_request_handler.text_dict['details'] = TEXT_DICT_DETAILS
    new_request_handler.text_dict['attachment'] = MENTOR_REQUEST_ATTACHMENT

    correct_response = SlackBuilder.mentor_request(MENTORS_INTERNAL_CHANNEL,
                                                   details=TEXT_DICT_DETAILS,
                                                   text=TEXT_DICT_MESSAGE,
                                                   attachment=MENTOR_REQUEST_ATTACHMENT,
                                                   matches=TEXT_DICT_MATCHES)

    new_request_handler.build_responses()
    # print(new_request_handler.response)

    assert correct_response in new_request_handler.response
