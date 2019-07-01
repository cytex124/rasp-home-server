import requests
from .models import Band, Proxy, Vote
from time import sleep
from random import randint


def vote_on_novarock_page():
    sleep(randint(0, 300))
    proxy = Proxy.get_random()
    proxy_url = proxy.url
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    headers = {
        'accept':  'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'content-type': 'multipart/form-data',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    payload = {
        '_dcbl_forms_uid': 'bandvoting0',
        'dsgvo_check': 'on'
    }

    bands = set()
    used_bands = []
    for i in range(5):
        payload, band = _add_band(payload, i + 1, used_bands)
        bands.add(band)

    session = requests.Session()
    response = session.post('https://www.novarock.at/form/bandvoting/', headers=headers, data=payload, proxies=proxies)

    vote = Vote.objects.create(proxy=proxy, response_code=response.status_code)
    for band in bands:
        vote.bands.add(band)


def _add_band(payload, index, used_bands):
    band = Band.get_random()
    if band.id in used_bands:
        return _add_band(payload, index, used_bands)
    else:
        used_bands.append(band.id)
        payload['choice{}'.format(index)] = band.choice_id
        payload['choice{}_hidden_value'.format(index)] = band.name
        return payload, band