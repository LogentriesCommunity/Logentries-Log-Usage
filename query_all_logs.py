import urllib
import json
import sys
import requests
import time
import csv
import time
from datetime import datetime


API_KEY = sys.argv[2]
now_millis = int(round(time.time() * 1000))
TO_TS = now_millis
FROM_TS = "1467500400000"# miliseconds 3rd July

SEARCH_QUERY = "where(/.*/) calculate(bytes)"
ACCOUNT_KEY = ''
HOST_NAMES_KEYS_DICT = {}
OUTFILE = open(sys.argv[3], 'w')
OUTFILE_WRITER = csv.writer(OUTFILE)
OUTFILE_WRITER.writerow(['Log Name', 'Query Result'])


def get_host_name():
    req = urllib.urlopen("http://api.logentries.com/" + ACCOUNT_KEY + '/hosts/')
    response = json.load(req)
    for hosts in response['list']:
        HOST_NAMES_KEYS_DICT[hosts['key']] = hosts['name']
    for k, v in HOST_NAMES_KEYS_DICT.iteritems():
        if v != r'Inactivity Alerts':
            del v
            get_log_name_and_key(k)


def get_le_url(url):
    header = {'x-api-key': API_KEY}
    return requests.get(url, headers=header)


def get_continuity_final_response(response):
    while True:
        response = get_le_url(response.json()['links'][0]['href'])
        if response.status_code != 200:
            return None
        if 'links' not in response.json():
            return response
        else:
            time.sleep(1)
            continue


def handle_response(resp):
    time.sleep(4)
    if resp.status_code == 200:
        return resp
    if resp.status_code == 202:
        return get_continuity_final_response(resp)
    if resp.status_code > 202:
        print 'Error status code ' + str(resp.status_code)
        return


def get_log_name_and_key(host_key):
    req = urllib.urlopen("http://api.logentries.com/" + ACCOUNT_KEY + '/hosts/' + host_key + '/')
    response = json.load(req)
    headers = {'x-api-key': API_KEY}

    for everylogkey in response['list']:

        print everylogkey['name']

        payload = {"logs": [str(everylogkey['key'])],
                   "leql": {"during": {"from": FROM_TS, "to": TO_TS},
                            "statement": SEARCH_QUERY}}

        url = "https://rest.logentries.com/query/logs/"
        results = requests.post(url, headers=headers, json=payload)
        results = handle_response(results)
        # if query is calculate(count) then: results.json()['statistics']['stats']['global_timeseries']['count']
        # if query is calculate(bytes) then: results.json()['statistics']['stats']['global_timeseries']['bytes']
        try:
            query_result = str(results.json()['statistics']['stats']['global_timeseries']['bytes'])
            print query_result
            OUTFILE_WRITER.writerow((everylogkey['name'], query_result))
        except KeyError as exception:
            print "*** Empty Result ***"


if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    get_host_name()
    OUTFILE.close()
