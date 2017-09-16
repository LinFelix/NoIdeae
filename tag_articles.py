import os
import sys
sys.path.append('libs/')
import reutherAPIwrapper
from class_parser import Article, ArticleData
from perm import queryPerm


class cleanData(object):
    def __init__(self, data_path, cleaned_data):
        self.data_path = data_path
        self.cleaned_data = cleaned_data
        if not os.path.exists(self.cleaned_data):
            os.makedirs(self.cleaned_data)
            
        i = 0
        done = False
        while not done:
            try:
                article_file = open(os.path.join(self.data_path, '{}.txt'.format(i)))
                self.clean_file(article_file, i)
                i = i + 1
            except IOError:
                done = True
                break


    def clean_file(self, article, i):
        cleaned_file = open(os.path.join(self.cleaned_data, 'cl{}.txt'.format(i)), 'w')

        for line in article:
            line = line.lstrip()
            if '<p>' in line:
                line = line.replace('<p>', '')
            if '</p>' in line:
                line = line.replace('</p>', '')
            if '<p/>' in line:
                line = line.replace('<p/>', '')
            cleaned_file.write(line)
        cleaned_file.close()



if __name__=='__main__':
    data_dir = 'raw_data'
    output_dir = 'data'
    clean_data = 'clean'

    print("Collecting articles...")
    reutherAPIwrapper.save_all_text(data_dir)
    print('Done.')
    print('Cleaning files...')
    cleanData(data_dir, clean_data)
    print('Done')
    print('Querying perm..')
    tagger = queryPerm(clean_data, output_dir)
    print('Done.')
    # Start parsing data
    art_data = ArticleData()
    art_data.parse_data(output_dir)
    print()


