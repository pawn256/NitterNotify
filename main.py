import os,sys
sys.path.append(os.environ['TOOLS_DIR'])

import Notify3
import requests
import time
from bs4 import BeautifulSoup

class NitterNotify:
    def __init__(self, userName):
        self.userName = userName
        self.url = 'https://nitter.net/{}'.format(userName)
        self.title = 'nitter {}'.format(userName) 
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
                }
        self.pinnedBody = ''
        self.tweetBody = ''

    def notify(self, title, body):
        objNotify=Notify3.Notify(title)
        objNotify.notify()
        objNotify.setText(body)
        objNotify.setButton()
        objNotify.wavplay()
        objNotify.start()

    def getPinnedTweet(self):
        req = requests.get(
                self.url,
                headers = self.headers
                )
        
        bs = BeautifulSoup(req.content,'lxml')
        tweetBody = bs.select('.tweet-body')
        if len(tweetBody) == 0: return ''

        pinned = tweetBody[0].select('.pinned')
        if len(pinned) == 0: return ''

        body = tweetBody[0].select('.tweet-content.media-body')
        if len(body) == 0: return ''

        bodyText = body[0].text
        if self.pinnedBody != bodyText:
            self.pinnedBody = bodyText
            self.notify(self.title + ' pinned', self.pinnedBody)

        return self.pinnedBody

    def getTweet(self):
        req = requests.get(
                self.url,
                headers = self.headers
                )
        
        bs = BeautifulSoup(req.content,'lxml')
        tweetBody = bs.select('.tweet-body')
        if len(tweetBody) == 0: return ''

        pinned = tweetBody[0].select('.pinned')
        body = None
        if len(pinned) >= 1: 
            if len(tweetBody) <= 1: return ''
            body = tweetBody[1].select('.tweet-content.media-body')
        else:
            body = tweetBody[0].select('.tweet-content.media-body')

        if body == None or len(body) == 0: return ''

        bodyText = body[0].text
        if self.tweetBody != bodyText:
            self.tweetBody = bodyText
            self.notify(self.title, self.tweetBody)

        return self.tweetBody

def main():
    userName = sys.argv[1]
    nitterNotify = NitterNotify(userName)
    while True:
        try:
            nitterNotify.getPinnedTweet()
        except Exception as e:
            print("getPinnedTweet:", e)

        try:
            nitterNotify.getTweet()
        except Exception as e:
            print("getTweet:", e)

        time.sleep(600)

if __name__ == '__main__':
    main()
