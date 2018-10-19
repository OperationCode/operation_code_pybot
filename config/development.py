from decouple import config

DEBUG = True

PORT = 5000

SLACK_TOKEN = config('DEV_BOT_TOKEN', default='token')
SLACK_VERIFICATION_TOKEN = config('DEV_AUTH_TOKEN', default='token')
SLACK_COMMUNITY_CHANNEL = config('DEV_PRIVATE_CHANNEL', default='community_channel')
SLACK_MENTORS_INTERNAL_CHANNEL = config('DEV_PRIVATE_CHANNEL', default='mentor_channel')

AIRTABLE_BASE_KEY = config('DEV_AIRTABLE_BASE_KEY', default='fake_airtable_base')
AIRTABLE_API_KEY = config('DEV_AIRTABLE_TOKEN', default='fake_airtable_key')
AIRTABLE_TABLE_NAME = 'Mentor Request'

DB_USERNAME = config('DEV_DB_USERNAME', default='')
DB_PASSWORD = config('DEV_DB_PASSWORD', default='')
DB_DIALECT = config('DEV_DB_DIALECT', default='sqlite')
DB_ADDR = config('DEV_DB_ADDR', default='dev.db')
DB_NAME = config('DEV_DB_NAME', default='')

GOOGLE_RECAPTCHA_SECRET = config('RECAPTCHA_SECRET')

GITHUB_JWT = config('GITHUB_JWT')
GITHUB_REPO_PATH = config('DEV_GITHUB_REPO_PATH')

OC_BACKEND_JWT_TOKEN = config('OC_BACKEND_JWT_TOKEN')
OC_BACKEND_URL = config('OC_BACKEND_URL')
