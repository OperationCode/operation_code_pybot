from typing import List
from time import time

from ocbot import AirTableBuilder
from ocbot.external.route_airtable import Airtable
from ocbot.external.route_slack import SlackBuilder, Slack

from .abc import RouteHandler
from ocbot.pipeline.utils import get_response_type, get_attachment_name, make_base_params


class MenteeClaimHandler(RouteHandler):
    """
    Handles the interactive message sent to the #community channel
    when a new member joins.

    Displays the user that claimed the greeting along with the option
    to un-claim
    """

    def __init__(self, *, event_dict: dict):
        self._user_id = event_dict['user']['id']
        self._user_name = event_dict['user']['name']
        self._event = event_dict
        self.click_type = get_response_type(self._event)
        self._record_id = get_attachment_name(self._event)
        super().__init__()

    def api_calls(self):
        user_info = Slack().user_info_from_id(slack_id=self._user_id)
        email = user_info['user']['profile']['email']
        self.api_dict['mentor_id'] = Airtable.mentor_id_from_slack_email(email)

    def database_calls(self):
        pass

    def build_templates(self):
        params = make_base_params(self._event)
        mentor_id = self.api_dict['mentor_id']
        # adjust button type
        if self.click_type == 'mentee_claimed':
            if mentor_id:
                params['attachments'] = self.mentee_claimed_attachments(self._record_id)
            else:
                attachments = self.mentee_unclaimed_attachment(self._record_id)
                attachments[0]['text'] = (f":warning: <@{self._user_id}>'s Slack Email not"
                                          " found in Mentor table. :warning:")
                params['attachments'] = attachments
        else:
            params['attachments'] = self.mentee_unclaimed_attachment(self._record_id)

        self.text_dict['message'] = params

    def build_responses(self):
        params = self.text_dict['message']
        mentor_id = self.api_dict['mentor_id']

        if self.click_type == 'mentee_claimed':
            self.include_resp(AirTableBuilder.claim_mentee, self._record_id, mentor_id)
        elif self.click_type == 'reset_claim_mentee':
            self.include_resp(AirTableBuilder.claim_mentee, self._record_id, '')

        self.include_resp(SlackBuilder.update, **params)

    def now(self):
        """
        This has to be pulled out into its own method so a mock can
        be injected for testing purposes
        """
        return int(time())

    def mentee_claimed_attachments(self, record: str) -> List[dict]:
        unix_time = self.now()
        return [
            {
                "text": f":100: Request claimed by <@{self._user_id}>:100:\n"
                        f"<!date^{unix_time}^Claimed at {{date_num}} {{time_secs}}|Failed to parse time>",
                "fallback": "",
                "color": "#3AA3E3",
                "callback_id": "claim_mentee",
                "attachment_type": "default",
                "actions": [{
                    'name': f'{record}',
                    "text": f"Reset claim",
                    "type": "button",
                    "style": "danger",
                    "value": "reset_claim_mentee",
                }]
            }
        ]

    def mentee_unclaimed_attachment(self, record: str) -> List[dict]:
        unix_time = self.now()
        return [
            {
                'text': f"Reset by <@{self._event['user']['id']}> at"
                        f" <!date^{unix_time}^ {{date_num}} {{time_secs}}|Failed to parse time>",
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
                        'value': 'mentee_claimed'

                    }
                ]

            }
        ]
