'''
Code to tag news articles

Command in terminal : python perm.py input output LZUy2XvmGgFwkO9BSXQ1SSLEDuQUjGrg
where input is the directory where you have all news articles in txt format
output is the directory where you get all tags of all news articles stored in json format

'''

import sys
import requests
import os
from pprint import pprint
import json

calais_url = 'https://api.thomsonreuters.com/permid/calais'


class queryPerm(object):
    def __init__(self, input_dir, output_dir, access_token="Jz5ghWp8LbjYHL83WECGF3AUXV3Xk8Jm"):
        #'LZUy2XvmGgFwkO9BSXQ1SSLEDuQUjGrg'):
        try:
            if not os.path.exists(input_dir):
                print('The file {} does not exist'.format(input_dir))
                return
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            headers = {'X-AG-Access-Token' : access_token, 'Content-Type' : 'text/raw', 'outputformat' : 'application/json'}
            self.sendFiles(input_dir, headers, output_dir)
        except:
            print('Error in connection')

    def sendFiles(self, files, headers, output_dir):
        is_file = os.path.isfile(files)
        if is_file == True:
            self.sendFile(files, headers, output_dir)
        else:
            for file_name in os.listdir(files):
                # if os.path.isfile(file_name):
                file_name = os.path.join(files, file_name)
                self.sendFile(file_name, headers, output_dir)
                # else:
                    # self.sendFiles(file_name, headers, output_dir)

    def sendFile(self, file_name, headers, output_dir):
        with open(file_name, 'rb') as input_data:
            response = requests.post(calais_url, data=input_data, headers=headers, timeout=80)
            # print('status code: {}'.format(response.status_code))
            content = response.text
            if response.status_code == 200:
                self.saveFile(file_name, output_dir, content)

    def saveFile(self, file_name, output_dir, content):
        output_file_name = os.path.basename(file_name[:-4]) + '.json'
        output_file = open(os.path.join(output_dir, output_file_name), 'wb')
        output_file.write(content.encode('utf-8'))
        output_file.close()

if __name__ == "__main__":
   perm = queryPerm()
