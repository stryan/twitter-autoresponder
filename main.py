import tweepy
import markovify
import sys
import threading
from keys import keys
from autoresponder import AutoResponder
class MainThread (threading.Thread):
    def __init__(self, threadID, name, bot):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.bot = bot
    
    def run(self):
        print "Running main loop"
        self.bot.main_loop()

def init_twitter(): 
    consumer_key = keys['consumer_key']
    consumer_secret = keys['consumer_secret']
    access_token = keys['access_token']
    access_token_secret = keys['access_token_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth) 

def init_model():
    filename = "tweetdb"
    dbfile = open("tweetdb")
    db = dbfile.read()
    model = markovify.NewlineText(db)
    return model 

def main():
    api = init_twitter()
    model = init_model()
    bot = AutoResponder(model,api, True)
    main_t = MainThread(1, "main", bot)
    main_t.start()
    main_t.join()

if __name__ == "__main__":
    main()

