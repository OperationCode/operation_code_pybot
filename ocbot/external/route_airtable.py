import logging

from ocbot.external import ResponseContainer
from requests import post, get, patch
from functools import partial
from config.all_config_loader import configs

logger = logging.getLogger(__name__)


class AirTableBuilder:
    BASE = configs['AIRTABLE_BASE_KEY']
    API_KEY = configs['AIRTABLE_API_KEY']
    MENTORS_TABLE_NAME = "Mentors"
    REQUEST_TABLE_NAME = "Mentor Request"
    services_id_to_service = {}

    @classmethod
    def record_to_service(cls, record: str) -> str:
        if not cls.services_id_to_service:
            cls.services_id_to_service = cls.get_translations()

        return cls.services_id_to_service[record]

    @classmethod
    def get_translations(cls):
        header = AirTableBuilder.build_auth_header()
        url = f'https://api.airtable.com/v0/{cls.BASE}/Services?fields%5B%5D=Name'
        res = get(url, headers=header)
        records = res.json()['records']
        return {record['id']: record['fields']['Name'] for record in records}

    @classmethod
    def entry(cls, params):
        return ResponseContainer(route='AirTable',
                                 method='raw',
                                 payload=dict(url=cls.build_url,
                                              json=params,
                                              headers=cls.build_auth_header()
                                              )
                                 )

    @classmethod
    def build_auth_header(cls):
        return {f'authorization': f"Bearer {cls.API_KEY}"}

    @classmethod
    def build_url(cls, table_name, record_id=None):
        url = f'https://api.airtable.com/v0/{cls.BASE}/{table_name}'
        if record_id:
            url += f'/{record_id}'
        return url

    @classmethod
    def claim_mentee(cls, record, mentor):
        return ResponseContainer(route='Airtable',
                                 method='patch',
                                 payload=dict(
                                     url=cls.build_url("Mentor Request", record),
                                     headers=cls.build_auth_header(),
                                     mentor=mentor
                                 ))


class Airtable:
    def __getattr__(self, name):
        """
        called when getattr(self, name) is not found
        """
        default = partial(self.default, name)
        return default

    def raw(self, params):
        try:
            post(**params)
        except Exception as error:
            raise Exception("Exception at airtable params\n"
                            f"{params}"
                            f"Exception value:"
                            f"{error}")

    @staticmethod
    def patch(payload: dict):
        url = payload['url']
        headers = payload['headers']
        mentor = [payload['mentor']] if payload['mentor'] else None
        data = {"fields": {
            "Mentor Assigned": mentor
        }}
        res = patch(url, json=data, headers=headers)
        logger.info(f'Airtable API call status: {res.status_code} | Content: {res.content}')

    @staticmethod
    def mentor_id_from_slack_username(username: str) -> str:
        url = AirTableBuilder.build_url("Mentors")
        params = {
            "filterByFormula": f"FIND(LOWER('{username}'), LOWER({{Slack Name}}))"
        }
        headers = AirTableBuilder.build_auth_header()
        res = get(url, headers=headers, params=params)
        if res.status_code == 200:
            records = res.json()['records']
            if records:
                return records[0]['id']
            else:
                return ''
        else:
            return ''

    @staticmethod
    def find_mentors_with_matching_skillsets(skillsetStr: str) -> list:
        url = AirTableBuilder.build_url("Mentors") + "?fields=Email&fields=Skillsets"
        headers = AirTableBuilder.build_auth_header()
        skillsets = skillsetStr.split(',')
        mentors = get(url, headers=headers).json()['records']
        partial_match = []
        complete_match = []
        try:
            for mentor in mentors:
                if all(skillset in mentor['fields']['Skillsets'] for skillset in skillsets):
                    complete_match.append(mentor['fields'])
                if any(mentor['fields'] not in complete_match and
                       skillset in mentor['fields']['Skillsets'] for skillset in skillsets):
                    partial_match.append(mentor['fields'])
        except Exception as e:
            logger.warning("Exception occurred while attempting to get matching mentors for skillsets : ", e)

        return complete_match or partial_match

    @staticmethod
    def mentor_id_from_slack_email(email: str) -> str:
        url = AirTableBuilder.build_url("Mentors")
        params = {
            "filterByFormula": f"FIND(LOWER('{email}'), LOWER({{Email}}))"
        }
        headers = AirTableBuilder.build_auth_header()
        res = get(url, headers=headers, params=params)
        if res.status_code == 200:
            records = res.json()['records']
            if records:
                return records[0]['id']
            else:
                return ''
        else:
            return ''

    def default(self, method, payload):
        raise NotImplemented
