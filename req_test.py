try:
    import urllib.parse as urllib
except ImportError:
    import urllib
import json
import requests
import os

class dataCollect(object):
    def __init__(self, url):
        self.url = url

    def fetch_data(self, values):
        data = urllib.urlencode(values)
        full_url = self.url + '?' + data
        response = requests.get(full_url)
        if response.ok:
            print("Page received.")
            return response.json()
        else:
            print("Impossible to load page.")
            return None

    def write_data(self, data, file_path):
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)

if __name__=='__main__':
    url = 'http://srgssr-prod.apigee.net/polis-api/Polis.Official'
    values = {'apikey' : 'uA9m9sTbOGNAsyDCIy4DtWQNV1udAV4p'}

    requester = dataCollect(url=url)
    data = requester.fetch_data(values=values)
    if data is not None:
        requester.write_data(data=data,
                             file_path='data.txt')
