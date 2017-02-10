import tweepy
import markovify
import sys
import threading
from keys import keys
from autoresponder import AutoResponder

class AutoThread (threading.Thread):
    def __init__(self, threadID, name, bot, event):
        threading.Thread.__init__(self)
        self.name = name
        self.threadID = threadID
        self.bot = bot;
        self.stopped = event
        self.counter = 0
    def run(self):
        while not self.stopped.wait(300):
            self.bot.respond_to_tweet()
            if (self.counter >= 12):
                self.counter = 0
                self.bot.new_tweet()
            else:
                self.counter = self.counter + 1

class MainThread (threading.Thread):
    def __init__(self, threadID, name, bot):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.autor = bot
        self.stopFlag = None
    def main_loop(self):
        while 1:
            sys.stdout.write('> ')
            cmd = raw_input()
            if cmd == "toggle_auto":
                if (self.stopFlag is not None):
                    print "auto mode disengaged"
                    self.stopFlag.set()
                    self.stopFlag = None
                    return
                print "auto mode engaged"
                self.autor.toggle_auto()
                self.stopFlag = threading.Event()
                auto_t = AutoThread(2, "auto", self.autor, self.stopFlag)
                auto_t.start()
            if cmd == "tweet":
                self.autor.new_tweet()
            if cmd == "respond":
                self.autor.respond_to_tweet()
            if cmd == "target":
                self.autor.target_tweet()
            if cmd == "toggle_dummy":
                self.autor.toggle_dummy()
            if cmd == "exit":
                if (self.stopFlag is not None):
                    self.stopFlag.set()
                self.autor.save_responses()
                return  
  
    def run(self):
        print "Running main loop"
        self.main_loop()

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
    accountname = keys['accountname']
    bot = AutoResponder(model,api, False, "imagedb", accountname)
    main_t = MainThread(1, "main", bot)
    main_t.start()
    main_t.join()

if __name__ == "__main__":
    main()

