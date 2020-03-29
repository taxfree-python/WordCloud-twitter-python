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

CK = CONFIG.CONSUMER_KEY
CS = CONFIG.CONSUMER_SECRET
AT = CONFIG.ACCESS_TOKEN
ATS = CONFIG.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK,CS,AT,ATS)

args = sys.argv
print('file_name= ' + args[1])
print('picture_name= ' + args[2])
csv_path = args[1] + '.csv'

url = 'https://api.twitter.com/1.1/search/tweets.json'

keyword = '#数理の翼Nセミナー'
params = {'q':keyword, 'count' : 100,'result_type':'recent'}
with open(csv_path,'w') as f:
    #twitter API part
    for j in range(1):
        res = twitter.get(url, params = params)
        if res.status_code == 200:
            n = 0
            timeline = json.loads(res.text)
            for twit in timeline['statuses']:
                if twit['text'] not in 'RT':
                    f.write(twit['text'])
                    print(twit['text'])
            print(len(timeline))

def counter(texts):
    t = Tokenizer()
    words_count = defaultdict(int)
    words = []
    for text in texts:
        tokens = t.tokenize(text)
        for token in tokens:
            #名詞抽出
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
#mask = np.array(Image.open('masks/wordcloud_07.png'))
wordcloud = WordCloud(background_color="white",font_path=fpath, width=1000, height=700,contour_width=1, contour_color='steelblue')
wordcloud.generate(text)

#save picture
picture_path = 'picture/' + args[3] + '.png'
wordcloud.to_file(picture_path)

#cd csv_file
file_cd = 'csv/' + csv_path
shutil.move(csv_path,file_cd)

#show picture
img = Image.open(picture_path)
img.show()