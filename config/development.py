from decouple import config

PORT = 5000

TOKEN = config('DEV_BOT_TOKEN', default='token')
VERIFICATION_TOKEN = config('DEV_AUTH_TOKEN', default='token')
COMMUNITY_CHANNEL = config('DEV_PRIVATE_CHANNEL', default='community_channel')
MENTORS_INTERNAL_CHANNEL = config('DEV_PRIVATE_CHANNEL', default='mentor_channel')

AIRTABLE_BASE_KEY = config('DEV_AIRTABLE_BASE_KEY', default='fake_airtable_base')
AIRTABLE_API_KEY = config('DEV_AIRTABLE_TOKEN', default='fake_airtable_key')
AIRTABLE_TABLE_NAME = 'Mentor Request'

DB_USERNAME = config('DEV_DB_USERNAME', default='')
DB_PASSWORD = config('DEV_DB_PASSWORD', default='')
DB_DIALECT = config('DEV_DB_DIALECT', default='sqlite')
DB_ADDR = config('DEV_DB_ADDR', default='dev.db')
DB_NAME = config('DEV_DB_NAME', default='')

PA_SSH_USERNAME = config('PA_SSH_USERNAME', default=None)
PA_SSH_PASSWORD = config('PA_SSH_PASSWORD', default=None)
PA_SSH_URL = config('PA_SSH_URL', default=None)
PA_SSH_REMOTE_BIND_ADDR = config('PA_PG_IP_ADDR', cast=str, default=None)
PA_SSH_REMOTE_BIND_PORT = config('PA_PG_PORT', cast=int, default=0)

RECAPTCHA_SECRET = config('RECAPTCHA_SECRET')
GITHUB_JWT = config('GITHUB_JWT')
GITHUB_REPO_PATH = config('DEV_GITHUB_REPO_PATH')

BACK_JWT_TOKEN = config('BACK_JWT_TOKEN')
OC_URL = config('OC_URL')
DEV_GITHUB_REPO_PATH = ''