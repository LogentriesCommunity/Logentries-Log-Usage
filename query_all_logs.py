import urllib
import json
import sys
import requests
import time
import csv


API_KEY = sys.argv[2]
now_millis = int(round(time.time() * 1000))
TO_TS = now_millis
date_time = sys.argv[4]#'dd.mm.yyyy'
time_patt = '%d.%m.%Y'
epoch = int(time.mktime(time.strptime(date_time, time_patt)))
FROM_TS = epoch * 1000

SEARCH_QUERY = "where(/.*/) calculate(bytes)"
ACCOUNT_KEY = ''
HOST_NAMES_KEYS_DICT = {}
OUTFILE = open(sys.argv[3], 'w')
OUTFILE_WRITER = csv.writer(OUTFILE)
OUTFILE_WRITER.writerow(['Log Set', 'Log Name', 'Query Result'])


def get_host_name():
    req = urllib.urlopen("https://api.logentries.com/" + ACCOUNT_KEY + '/hosts/')
    response = json.load(req)
    for hosts in response['list']:
        HOST_NAMES_KEYS_DICT[hosts['key']] = hosts['name']
    for k, v in HOST_NAMES_KEYS_DICT.iteritems():
        if v != r'Inactivity Alerts':
            get_log_name_and_key(k, v)
        else:
            pass


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


def post_query_to_le(hostkey):
    headers = {'x-api-key': API_KEY}
    payload = {"logs": [hostkey],
               "leql": {"during": {"from": FROM_TS, "to": TO_TS},
                        "statement": SEARCH_QUERY}}

    url = "https://rest.logentries.com/query/logs/"
    return requests.post(url, headers=headers, json=payload)


def handle_response(resp, log_key):
    time.sleep(0.5)
    if resp.status_code == 200:
        return resp
    elif resp.status_code == 202:
        print "Polling after 202"
        return get_continuity_final_response(resp)
    elif resp.status_code == 503:
        print "Retrying after 503 code"
        retried_response = post_query_to_le(log_key)
        return handle_response(retried_response, log_key)
    elif resp.status_code > 202:
        print 'Error status code ' + str(resp.status_code)
        return


def get_log_name_and_key(host_key, host_name):
    req = urllib.urlopen("http://api.logentries.com/" + ACCOUNT_KEY + '/hosts/' + host_key + '/')
    response = json.load(req)
    for everylogkey in response['list']:
        if not everylogkey['key']:
            continue

        print everylogkey['name']

        results1 = post_query_to_le(str(everylogkey['key']))
        results = handle_response(results1, str(everylogkey['key']))
        # if query is calculate(count) then: results.json()['statistics']['stats']['global_timeseries']['count']
        # if query is calculate(bytes) then: results.json()['statistics']['stats']['global_timeseries']['bytes']
        try:
            if len(results.json()['statistics']['stats']['global_timeseries']) > 0:
                query_result = str(results.json()['statistics']['stats']['global_timeseries']['bytes'])
            else:
                query_result = 0
            print query_result
            OUTFILE_WRITER.writerow((host_name, everylogkey['name'], query_result))
        except KeyError as exception:
            print "Empty"


if __name__ == '__main__':
    ACCOUNT_KEY = sys.argv[1]
    get_host_name()
    OUTFILE.close()
    print "csv result file generated. all done."
