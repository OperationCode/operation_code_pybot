from functools import lru_cache
from typing import List

from ocbot.external.route_airtable import AirTableBuilder, Airtable
from ocbot.external.route_slack import SlackBuilder, Slack
from ocbot.pipeline.handlers.abc import RouteHandler
from config.all_config_loader import configs

MENTORS_INTERNAL_CHANNEL = configs['SLACK_MENTORS_INTERNAL_CHANNEL']


class NewAirtableRequestHandler(RouteHandler):

    def __init__(self, *, event_dict):
        self._user_email = event_dict['Email']
        self._event = event_dict
        super().__init__()

    def api_calls(self):
        """
        Queries slack for user ID to be linked to their account (@user)
        If not found defaults to displaying the provided Slack Username in plaintext
        :return:
        """
        response = Slack().user_id_from_email(self._user_email)
        if response['ok']:
            self.api_dict['user'] = f"<@{response['user']['id']}>"
        else:
            self.api_dict['user'] = self._event['Slack User']

        matches = Airtable.find_mentors_with_matching_skillsets(self._event['Skillsets'])
        ids = self.get_mentor_slack_ids(matches)

        self.api_dict['matches'] = ids

    def database_calls(self):
        pass

    def build_templates(self):
        service = AirTableBuilder.record_to_service(self._event['Service'])
        if 'Skillsets' not in self._event:
            self._event['Skillsets'] = 'None given'

        self.text_dict['message'] = f"User {self.api_dict['user']} has requested a mentor for {service}\n\n" \
                                    f"Requested Skillset(s): {self._event['Skillsets'].replace(',', ', ')}"
        self.text_dict['attachment'] = initial_claim_button(self._event['Record'])
        if 'Details' in self._event:
            self.text_dict['details'] = f"Additional details: {self._event['Details']}"
        else:
            self.text_dict['details'] = f"Additional details: None Given"

        self.text_dict['details'] = f"Additional details: {self._event['Details']}"
        self.text_dict['matches'] = "Mentors matching all or some of the requested skillsets: " + ' '.join(
            self.api_dict['matches'])

    def build_responses(self):
        message_text = self.text_dict['message']
        attachment = self.text_dict['attachment']
        details_text = self.text_dict['details']
        matches = self.text_dict['matches']

        self.include_resp(SlackBuilder.mentor_request, MENTORS_INTERNAL_CHANNEL, details=details_text,
                          attachment=attachment,
                          matches=matches,
                          text=message_text)

    @staticmethod
    def get_mentor_slack_ids(matches: list) -> list:
        ids = []
        for mentor in matches:
            res = NewAirtableRequestHandler.check_user_id_cache(mentor['Email'])
            if res['ok']:
                ids.append(f"<@{res['user']['id']}>")
        return ids

    @staticmethod
    @lru_cache(64)
    def check_user_id_cache(email):
        return Slack().user_id_from_email(email)


def initial_claim_button(record) -> List[dict]:
    return [
        {
            'text': '',
            'fallback': '',
            'color': '#3AA3E3',
            'callback_id': 'claim_mentee',
            'attachment_type': 'default',
            'actions': [
                {
                    'name': f'{record}',
                    'text': 'Claim Mentee',
                    'type': 'button',
                    'style': 'primary',
                    'value': f'mentee_claimed',
                }
            ]

        }
    ]
