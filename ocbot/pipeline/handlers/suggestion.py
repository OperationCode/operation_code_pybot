from ocbot.external.route_slack import Slack, SlackBuilder

from .abc import RouteHandler
from config.all_config_loader import configs

COMMUNITY_CHANNEL = configs['SLACK_COMMUNITY_CHANNEL']

class SuggestionHandler(RouteHandler):
    """
        Receives the event when a user submits a suggestion for a new help topic and
        posts it to the #community channel
        :param event_dict:
        :type dict
        """
    _message = (":exclamation:<@{user_id}>"
                " just submitted a suggestion for a help topic:exclamation:\n-- "
                "{suggestion}")

    def __init__(self, *, event_dict):
        self._user_id = event_dict['user']['id']
        self._event = event_dict
        super().__init__()

    def api_calls(self):
        # slack api call for user_name
        self.api_dict['real_name'] = Slack().user_name_from_id(self._user_id)

    # TODO have bot look through resources for this item
    # TODO to get additional items
    def database_calls(self):
        pass

    def build_templates(self):
        suggestion = self._event['submission']['suggestion']
        self.text_dict['message'] = self._message.format(user_id=self._user_id, suggestion=suggestion)

    def build_responses(self):
        suggestion = self.text_dict['message']

        self.include_resp(SlackBuilder.message, COMMUNITY_CHANNEL, text=suggestion)
