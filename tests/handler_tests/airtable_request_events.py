NEW_AIRTABLE_REQUEST_JSON = {
    "Skillsets": "C / C++,Web (Frontend Development),Mobile (iOS),Java,DevOps",
    "Slack User": "ic4rusX",
    "Details": " Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin blandit porttitor nulla eu consectetur."
               " Maecenas consectetur erat at odio iaculis, ac auctor nunc imperdiet. Sed neque quam, cursus eget nunc"
               " et, viverra gravida justo. Vivamus pharetra magna vel leo rutrum imperdiet. Vestibulum tempus non leo"
               " vestibulum iaculis. Ut nec lacinia elit, viverra vulputate tortor. Phasellus eu luctus odio."
               " Vestibulum accumsan est sed metus dignissim, quis sollicitudin diam posuere. Duis ullamcorper"
               " ante vel vulputate semper. Aliquam viverra, lorem sit amet tristique consequat, velit tortor"
               " lacinia sem, sed placerat nisi sapien rutrum lacus. Mauris vehicula purus mi. Integer feugiat "
               "consectetur elit, ac interdum turpis condimentum ut. Pellentesque sollicitudin est nunc, non accumsan"
               " metus laoreet nec.\n\nPellentesque rhoncus iaculis felis. Donec efficitur bibendum arcu, sed varius "
               "orci bibendum nec. Morbi laoreet nunc nec urna pharetra viverra. Nulla vel magna ex. Fusce semper nisl"
               " commodo nulla tempus, nec aliquam libero bibendum. Proin eleifend odio nec augue facilisis, nec"
               " faucibus tortor venenatis. Pellentesque pulvinar erat nec justo bibendum blandit.\n\nDonec ut libero"
               " a ex posuere euismod. Cras vitae turpis sit amet magna egestas vehicula. Maecenas interdum commodo"
               " quam, vitae ornare mauris viverra vel. In vestibulum enim pulvinar, pharetra augue a, tempor felis."
               " Proin vel cursus tellus. Quisque eget mauris neque. Cras eu pharetra leo. Nam nulla tortor, imperdiet"
               " sit amet dictum eu, mollis id ante. ",
    "Service": "recry8s14qGJhHeOC",
    "Email": "ic4rusX@gmail.com",
    "Record": "someRecId'"
}

USER_ID_FROM_EMAIL_RESPONSE = {'ok': True, 'user': {'id': 'AGF2354'}}

TEXT_DICT_MESSAGE = "User <@AGF2354> has requested a mentor for General Guidance - Slack Chat Given Skillset(s): C / " \
                    "C++,Web (Frontend Development),Mobile (iOS),Java,DevOps View requests: " \
                    "<https://airtable.com/tbl9uQEE8VeMdNCey/viwYzYa4J9aytVB4B|Airtable> Please reply to the channel " \
                    "if you'd like to be assigned to this request."

TEXT_DICT_DETAILS = 'Additional details:  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin blandit ' \
                    'porttitor nulla eu consectetur. Maecenas consectetur erat at odio iaculis, ac auctor nunc ' \
                    'imperdiet. Sed neque quam, cursus eget nunc et, viverra gravida justo. Vivamus pharetra magna ' \
                    'vel leo rutrum imperdiet. Vestibulum tempus non leo vestibulum iaculis. Ut nec lacinia elit, ' \
                    'viverra vulputate tortor. Phasellus eu luctus odio. Vestibulum accumsan est sed metus dignissim, ' \
                    'quis sollicitudin diam posuere. Duis ullamcorper ante vel vulputate semper. Aliquam viverra, ' \
                    'lorem sit amet tristique consequat, velit tortor lacinia sem, sed placerat nisi sapien rutrum ' \
                    'lacus. Mauris vehicula purus mi. Integer feugiat consectetur elit, ac interdum turpis ' \
                    'condimentum ut. Pellentesque sollicitudin est nunc, non accumsan metus laoreet nec. Pellentesque ' \
                    'rhoncus iaculis felis. Donec efficitur bibendum arcu, sed varius orci bibendum nec. Morbi ' \
                    'laoreet nunc nec urna pharetra viverra. Nulla vel magna ex. Fusce semper nisl commodo nulla ' \
                    'tempus, nec aliquam libero bibendum. Proin eleifend odio nec augue facilisis, nec faucibus ' \
                    'tortor venenatis. Pellentesque pulvinar erat nec justo bibendum blandit. Donec ut libero a ex ' \
                    'posuere euismod. Cras vitae turpis sit amet magna egestas vehicula. Maecenas interdum commodo ' \
                    'quam, vitae ornare mauris viverra vel. In vestibulum enim pulvinar, pharetra augue a, ' \
                    'tempor felis. Proin vel cursus tellus. Quisque eget mauris neque. Cras eu pharetra leo. Nam ' \
                    'nulla tortor, imperdiet sit amet dictum eu, mollis id ante.'

MENTOR_REQUEST_ATTACHMENT = [
    {
        'text': '',
        'fallback': '',
        'color': '#3AA3E3',
        'callback_id': 'claim_mentee',
        'attachment_type': 'default',
        'actions': [
            {
                'name': 'fakerec',
                'text': 'Claim Mentee',
                'type': 'button',
                'style': 'primary',
                'value': f'mentee_claimed',
            }
        ]

    }
]

CLAIM_MENTEE_EVENT = {'type': 'interactive_message',
                      'actions': [{'name': 'rec7pRh2FwyO4nP2W', 'type': 'button', 'value': 'mentee_claimed'}],
                      'callback_id': 'claim_mentee', 'team': {'id': 'T8M8SQEN7', 'domain': 'test'},
                      'channel': {'id': 'G8NDRJJF9', 'name': 'privategroup'},
                      'user': {'id': 'U11111', 'name': 'tester'},
                      'action_ts': '1521402127.915363', 'message_ts': '1521402116.000129', 'attachment_id': '1',
                      'token': 'faketoken', 'is_app_unfurl': False, 'original_message': {
        'text': 'User <@U8N6XBL7Q> has requested a mentor for General Guidance - Slack Chat\n\nGiven Skillset(s): None given\n\nView requests: <https://airtable.com/tbl9uQEE8VeMdNCey/viwYzYa4J9aytVB4B|Airtable>',
        'username': 'test2-bot', 'bot_id': 'B8N6Z8M8E',
        'attachments': [
            {'callback_id': 'claim_mentee', 'id': 1, 'color': '3AA3E3', 'actions': [
                {'id': '1', 'name': 'rec7pRh2FwyO4nP2W', 'text': 'Claim Mentee', 'type': 'button',
                 'value': 'mentee_claimed', 'style': 'primary'}]}], 'type': 'message', 'subtype': 'bot_message',
        'thread_ts': '1521402116.000129', 'reply_count': 1, 'replies': [{'user': 'B00', 'ts': '1521402117.000015'}],
        'subscribed': False, 'unread_count': 1, 'ts': '1521402116.000129'},
                      'response_url': 'https://hooks.slack.com/actions/T8M8SQEN7/332727073942/JPnXPwSk8A5jffzf0DHuSnhS',
                      'trigger_id': '331226307360.293298830755.c73cad81aa525200275c2868dd168ab0'}

RESET_MENTEE_CLAIM_EVENT = {'type': 'interactive_message',
                            'actions': [{'name': 'rec7pRh2FwyO4nP2W', 'type': 'button', 'value': 'reset_claim_mentee'}],
                            'callback_id': 'claim_mentee', 'team': {'id': 'T8M8SQEN7', 'domain': 'test'},
                            'channel': {'id': 'G8NDRJJF9', 'name': 'privategroup'},
                            'user': {'id': 'U11111', 'name': 'tester'}, 'action_ts': '1521403472.901817',
                            'message_ts': '1521402116.000129', 'attachment_id': '1',
                            'token': 'faketoken', 'is_app_unfurl': False, 'original_message': {
        'text': 'User <@U8N6XBL7Q> has requested a mentor for General Guidance - Slack Chat\n\nGiven Skillset(s): None given\n\nView requests: &lt;https://airtable.com/tbl9uQEE8VeMdNCey/viwYzYa4J9aytVB4B|Airtable&gt;',
        'username': 'test2-bot', 'bot_id': 'B8N6Z8M8E', 'attachments': [{'callback_id': 'claim_mentee',
                                                                         'text': ':100: Request claimed by <@U8N6XBL7Q>:100:\n<!date^1521402131^Greeted at {date_num} {time_secs}|Failed to parse time>',
                                                                         'id': 1, 'color': '3AA3E3', 'actions': [
                {'id': '1', 'name': 'rec7pRh2FwyO4nP2W', 'text': 'Reset claim', 'type': 'button',
                 'value': 'reset_claim_mentee', 'style': 'danger'}]}], 'type': 'message', 'subtype': 'bot_message',
        'thread_ts': '1521402116.000129', 'reply_count': 1, 'replies': [{'user': 'B00', 'ts': '1521402117.000015'}],
        'subscribed': False, 'unread_count': 1, 'ts': '1521402116.000129'},
                            'response_url': 'https://hooks.slack.com/actions/T8M8SQEN7/331230500336/J5MfM0OC6I37iV9xQSPqQ2UD',
                            'trigger_id': '332007136373.293298830755.614be10d27ebd4e3d22af708906f27e0'}

INVALID_MENTOR_ID_TEXT = f":warning: <@U11111>'s Slack Email not found in Mentor table. :warning:"

RESET_MENTEE_ATTACHMENT = [{'text': 'Reset by <@U11111> at <!date^11111^ {date_num} {time_secs}|Failed to parse time>',
                            'fallback': '', 'color': '#3AA3E3', 'callback_id': 'claim_mentee',
                            'attachment_type': 'default', 'actions': [
        {'name': 'rec7pRh2FwyO4nP2W', 'text': 'Claim Mentee', 'type': 'button', 'style': 'primary',
         'value': 'mentee_claimed'}]}]

SLACK_USER_INFO = {'user': {'profile': {'email': 'fake@email.com'}}}
