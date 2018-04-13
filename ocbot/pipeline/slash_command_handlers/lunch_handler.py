import requests
from zipcodes import is_valid
from random import randint

import logging

logger = logging.getLogger(__name__)


def random_zip():
    random_zip = 0
    while not is_valid(str(random_zip)):
        range_start = 10 ** (4)
        range_end = (10 ** 5) - 1
        random_zip = randint(range_start, range_end)

    return str(random_zip)


def within_lunch_range(input_number):
    return int(input_number) <= 30


def two_params(first_param, second_param):
    if is_valid(first_param) and within_lunch_range(second_param):
        return {'location': first_param, 'range': second_param}
    else:
        return {'location': random_zip(), 'range': '20'}


def split_params(param_text):
    if not param_text:  # no params, default random zip code, 20 miles
        return {'location': random_zip(), 'range': '20'}

    params = param_text.split()

    if len(params) == 2:  # two values
        return two_params(params[0], params[1])

    if len(params) == 1 and is_valid(params[0]):  # one value
        return {'location': params[0], 'range': '20'}

    else:
        return {'location': random_zip(), 'range': '20'}


def get_random_lunch(lunch_response):
    number_locs = len(lunch_response['businesses'])

    selected_loc = randint(0, number_locs - 1)
    return lunch_response['businesses'][selected_loc]


def build_response_text(loc_dict):
    return f'The Wheel of Lunch has selected {loc_dict["name"]} at {" ".join(loc_dict["location"]["display_address"])}'


def create_lunch_event(request):
    param_dict = create_lunch_eventt = split_params(request.get('text'))
    params = (
        ('zip', f'{param_dict["location"]}^'),
        ('query', 'lunch^'),
        ('radius', f'{param_dict["range"]}'),
    )
    response = requests.get('https://wheelof.com/lunch/yelpProxyJSON.php', params=params)
    loc = get_random_lunch(response.json())
    logger.info(f"location selected for {request['user_name']}: {loc}")
    return build_response_text(loc)


if __name__ == '__main__':
    print(create_lunch_event({'text': '80020 20'}))
    print(create_lunch_event({'text': '20'}))
