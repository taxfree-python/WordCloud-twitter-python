#import
import json
import CONFIG
from requests_oauthlib import OAuth1Session
from janome.tokenizer import Tokenizer
import csv
from wordcloud import WordCloud
from collections import Counter, defaultdict
from time import sleep
import shutil
import sys
from PIL import Image
#import numpy as np

#認証
CK = CONFIG.CONSUMER_KEY
CS = CONFIG.CONSUMER_SECRET
AT = CONFIG.ACCESS_TOKEN
ATS = CONFIG.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK,CS,AT,ATS)

#parameter-required
args = sys.argv
print('screen name = ' + args[1])
print('file name = ' + args[2])
print('picture name = ' + args[3])
csv_path = args[2] + '.csv'
#mask_path = ('mask_path = ' + args[4])

url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

params = {'screen_name':args[1],'exclude_replies':False,'include_rts':True,'count':200}

f_out = open(csv_path,'w')

#twitter API part
for j in range(100):
    res = twitter.get(url, params = params)

    if res.status_code == 200:

        #count API
        limit = res.headers['x-rate-limit-remaining']
        print("API remain: " + limit)
        if limit == 1:
            sleep(60*15)

        n = 0
        timeline = json.loads(res.text)
        for i in range(len(timeline)):
            if i != len(timeline)-1:
                f_out.write(timeline[i]['text'] + '\n')
            else:
                f_out.write(timeline[i]['text'] + '\n')

                params['max_id'] = timeline[i]['id']-1
f_out.close()

#形態素解析 janome
def counter(texts):
    t = Tokenizer()
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            #Noun extraction
            pos = token.part_of_speech.split(',')[0]
            if pos in ['名詞']:
                if token.base_form not in ['こと','よう','そう','RT','それ','これ','ツイート','リプライ','とき','ところ','さん','もの','ため','twitter']:
                    words_count[token.base_form] += 1
                    words.append(token.base_form)
    return words_count, words

with open(csv_path,'r') as f:
    reader = csv.reader(f, delimiter='\t')
    texts = []
    for row in reader:
        if(len(row) > 0):

            text = row[0].split('http')
            texts.append(text[0])

words_count,words = counter(texts)
text = ' '.join(words)

#wordcloud
fpath = 'fonts/ipagp.ttf'
#mask = np.array(Image.open(mask_path))
wordcloud = WordCloud(background_color="black",font_path=fpath, width=1000, height=700,contour_width=1, contour_color='steelblue')
wordcloud.generate(text)

#save picture
picture_path = 'pictures/' + args[3] + '.png'
wordcloud.to_file(picture_path)

#cd csv_file
file_cd = 'csv/' + csv_path
shutil.move(csv_path,file_cd)

#show picture
img = Image.open(picture_path)
img.show()
