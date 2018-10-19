from ocbot.external.route_slack import SlackBuilder, Slack
from .abc import RouteHandler
from ocbot.pipeline.utils import needs_greet_button
from config.all_config_loader import configs

COMMUNITY_CHANNEL = configs['SLACK_COMMUNITY_CHANNEL']


class NewMemberHandler(RouteHandler):
    """
        Invoked when a new user joins and a team_join event is received.
        DMs the new user with the welcome message and help menu as well as pings
        the #community channel with a new member notification
        :param event_dict: dict
    """

    def __init__(self, *, event_dict):
        event_dict = event_dict['event']
        self.user_id = event_dict['user']['id']
        self._event = event_dict
        super().__init__()

    def api_calls(self):
        # slack api call for user_name
        self.api_dict['real_name'] = Slack().user_name_from_id(self.user_id)

    # TODO call database
    def database_calls(self):
        # database user call
        # self.db_dict['interests'] = self.db_call_interests()
        pass

    def process_db_response(self):
        built_resources = base_resources
        if not self.db_dict:
            built_resources['attachments'][0]['actions'] = default_interest
        return built_resources

    def build_templates(self):
        self.text_dict['message'] = text_greet.format(real_name=self.api_dict['real_name'])
        self.text_dict['resource'] = self.process_db_response()
        self.text_dict['community'] = f":tada: <@{self.user_id}> has joined! :tada:"
        self.text_dict['attach'] = needs_greet_button()
        pass

    def build_responses(self):
        message_text = self.text_dict['message']
        built_resource = self.text_dict['resource']
        community = self.text_dict['community']
        attachments = self.text_dict['attach']

        if 'channel_id' in self._event:
            channel = self._event['channel_id']
        else:
            channel = COMMUNITY_CHANNEL

        self.include_resp(SlackBuilder.message, self.user_id, text=message_text)
        self.include_resp(SlackBuilder.message, self.user_id, **external_buttons)
        self.include_resp(SlackBuilder.message, self.user_id, **built_resource)
        self.include_resp(SlackBuilder.message, channel, text=community, attachments=attachments)


text_greet = ("Hi {real_name},\n\n Welcome to Operation Code! I'm a bot designed to help answer questions and "
              "get you on your way in our community.\n\n Our goal here at Operation Code is to get veterans and "
              "their families started on the path to a career in programming. We do that through providing you with "
              "scholarships, mentoring, career development opportunities, conference tickets, and more!\n")

external_buttons = {
    "text": ("Much of the provided aid requires veteran or military spouse status. Please verify your status on your "
             "profile at https://operationcode.org/ if you haven't already."
             "\n\nYou're currently in Slack, a chat application that serves as the "
             "hub of Operation Code. If you're visiting us via your browser, Slack provides a stand alone program to "
             "make staying in touch even more convenient.\n\nAll active Operation Code projects are located on our "
             "source control repository. Our projects can be viewed on GitHub\n\n Lastly, please take a moment to "
             "review our Code of Conduct."),
    "attachments": [
        {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "external_buttons",
            "attachment_type": "default",
            "actions": [
                ### Taken out until backend endpoint to query veteran status is implemented
                # {
                #     "name": "verify",
                #     "text": "Verify Veteran Status",
                #     "type": "button",
                #     "value": "verify",
                #     "url": "https://operationcode.org/profile",
                #     "style": "primary"
                # },
                {
                    "name": "github",
                    "text": "GitHub",
                    "type": "button",
                    "value": "github",
                    "url": "https://github.com/OperationCode"
                },
                {
                    "name": "download",
                    "text": "Slack Client",
                    "type": "button",
                    "value": "download",
                    "url": "https://slack.com/downloads"
                },
                {
                    "name": "code_of_conduct",
                    "text": "Code of Conduct",
                    "type": "button",
                    "value": "code_of_conduct",
                    "url": "https://github.com/OperationCode/community/blob/master/code_of_conduct.md"
                }
            ]
        }
    ]
}

default_interest = [
    {
        "name": "javascript",
        "text": "JavaScript",
        "type": "button",
        "value": "javascript"
    },
    {
        "name": "python",
        "text": "Python",
        "type": "button",
        "value": "python"
    },
    {
        "name": "ruby",
        "text": "Ruby",
        "type": "button",
        "value": "ruby"
    },
    # {
    #     "name": "webdev",
    #     "text": "Web Dev",
    #     "type": "button",
    #     "value": "webdev"
    # }

]

base_resources = {
    "text": "We recommend the following resources.",
    "attachments": [
        {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "resource_buttons",
            "attachment_type": "default",
            "actions": None  # add in builder step
        },
        {
            "text": "",
            "fallback": "",
            "color": "#3AA3E3",
            "callback_id": "suggestion",
            "attachment_type": "default",
            "actions": [
                {
                    "name": "suggestion_button",
                    "text": "Are we missing something? Click!",
                    "type": "button",
                    "value": "suggestion_button"
                }
            ]
        }
    ]
}
