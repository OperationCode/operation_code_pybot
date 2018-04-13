# [OperationCodePyBot](https://github.com/OperationCode/operation_code_pybot)

[![Build Status](https://travis-ci.org/OperationCode/operationcode_pyback.svg?branch=master)](https://travis-ci.org/OperationCode/operationcode_pyback)

OperationCode PyBot is a python implementation slack chat bot built to deal with the [Slack API](https://api.slack.com).

## Current Version

### Integrating new members into our community.

When we have new members join this application will serve as a tool to integrate them, and interface with all the resources we offer.

Currently we offer integration with the slack Events API. When a new member joins the team slack sends events for all events we are subscribed to. These events are processed to provide information to the user and perform actions to assist the operation code leadership team. Current functionality includes:

* Contact new members with the new member information including resources, slack client, and information about our code of conduct.
* Connects the member to a method to request a new mentor
* Contacts the \# community channel and informs them of a new member
* Allows an individual to claim the ability to greet the new member.

## Version

Due to the [PEP 404](https://www.python.org/dev/peps/pep-0404/) announcement support of python 3 will be the standard. The initial release will be with 3.6.X.

## Resources

* [Slack Bot Tutorial](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html)
* [Slack Events API Framework](https://github.com/slackapi/python-slack-events-api)
* [Python Slack Client](https://github.com/slackapi/python-slackclient)
* [Slack RTM API Framework](https://github.com/slackapi/python-rtmbot)
* [Slack API/Documentation](https://api.slack.com/apps/A7NGBPBUL/general)

## Future Progress

In the future we wish to incorporate more methods to help individuals and have the slack bot serve as a tool outside of greeting new members.

Planned features:

* Slack slash with user group functionality
* Data collection of interactions
* Connect to @aaron 's resource.yml with interface for easily providing new resource content.
* Connect to Github and Airtable APIs to monitor progress and send data to mentor table
* Connect to backend table and integrate verified ID.me status into the resource process.

## Contributing

Bug reports and pull requests are welcome on [Github](https://github.com/OperationCode/operation_code_pybot). This project is intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the [Contributor Covenant](http://contributor-covenant.org) code of conduct. If you wish to assist, join the [\#new-team-rewrite](https://operation-code.slack.com/messages/C7NJLCCMB/) rewrite to learn how to contribute.

## License

This package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
