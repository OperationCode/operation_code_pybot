import json
import pprint
import urllib.parse

import requests
from flask import jsonify

from config.all_config_loader import configs

recaptcha_secret = configs['GOOGLE_RECAPTCHA_SECRET']
github_jwt = configs['GITHUB_JWT']
repo_path = configs['GITHUB_REPO_PATH']


def verify_recaptcha(ip_value, recaptcha_value):
    req = requests.post('https://www.google.com/recaptcha/api/siteverify',
                        data={'secret': recaptcha_secret,
                              'response': recaptcha_value,
                              'remoteip': ip_value})

    return req.json().get('success', False)


def handle_recaptcha_and_errors(request, imagefile):
    request_dict = request.form.to_dict()

    recaptcha_val = request_dict.pop('g-recaptcha-response')
    ip_value = request.remote_addr
    if verify_recaptcha(ip_value, recaptcha_val):
        res = create_issue(request_dict, imagefile.filename, url_root=request.url_root)
        print(res.__dict__)
        if res.status_code == 201:
            return jsonify(
                {"redirect": f'https://github.com/{repo_path}/issues', 'code': 302})
    return ''


def create_issue(request_dict, logo, url_root):
    url = f'https://api.github.com/repos/{repo_path}/issues'
    headers = {"Authorization": f"Bearer {github_jwt}"}

    params = make_params(**request_dict, url_root=url_root, school_logo=logo)
    pprint.pprint(params)
    res = requests.post(url, headers=headers, data=json.dumps(params))
    pprint.pprint(res)
    return res


def make_params(name, url, address1, address2, city, state, zipcode, country, rep_name,
                rep_email, school_logo, url_root, fulltime=False, hardware=False, has_online=False, online_only=False,
                va_accepted=False, is_mooc=False, with_housing=False, g_captcha_response=False) -> dict:
    fulltime = False if not fulltime else True
    hardware = False if not hardware else True
    has_online = False if not has_online else True
    online_only = False if not online_only else True
    va_accepted = False if not va_accepted else True
    is_mooc = False if not is_mooc else True
    with_housing = False if not with_housing else True

    urlified_logo_url = urllib.parse.quote(school_logo)

    users_to_notify = ['hpjaj', 'wimo7083', 'jhampton', 'kylemh', 'davidmolina', 'nellshamrell', 'hollomancer',
                       'maggi-oc']
    # users_to_notify = ['wimo7083', 'AllenAnthes']
    notify_users = ''.join([f'@{user} ,' for user in users_to_notify])
    data_values = ({
        'title': f'New Code School Request: {name}',
        'body': (
            f"Name: {name}\n"
            f"url: {url}\n"
            f"full_time: {fulltime}\n"
            f"hardware_included: {hardware}\n"
            f"has_online: {has_online}\n"
            f"online_only: {online_only}\n"
            f"va_accepted: {va_accepted}\n"
            f"mooc: {is_mooc}\n"
            f"with_housing: {with_housing}\n"
            f"address1: {address1}\n"
            f"address2: {address2}\n"
            f"city: {city}\n"
            f"state: {state}\n"
            f"country: {country}\n"
            f"zip: {zipcode}\n\n"
            f"rep name: {rep_name}\n"
            f"rep email: {rep_email}\n"
            f"logo:\n ![school-logo]({url_root}images/{urlified_logo_url})\n"
            # f"logo: ![school-logo](https://pybot.ngrok.io/images/{urlified_logo_url})\n"

            'This code school is ready to be added/updated:\n'
            f"{notify_users}\n"
            "Please close this issue once you've added/updated the code school."

        )
    })
    return data_values
