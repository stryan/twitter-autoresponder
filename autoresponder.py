import sys
import tweepy
import json
import os
import pickle

class AutoResponder():
    def __init__(self,model,api, dummy):
        self.model = model
        self.api = api
        self.dummy = dummy
        self.name = "@saintstevebot"
        if os.path.isfile('responded.txt'):
            with open('responded.txt','rb') as fp:
                    self.responses = pickle.load(fp)
        else:
            self.responses = []

    def new_tweet(self):
        sentence = self.model.make_short_sentence(140)
        print "Tweeting: " + sentence
        if (not self.dummy):
            self.api.update_status(sentence)

    def respond_to_tweet(self):
        current_twts = self.api.home_timeline()
        for tweet in current_twts:
            if tweet.text.find(self.name) != -1 and tweet.id not in self.responses:
                uname = tweet.user.screen_name
                limit = len(uname) + 2
                sentence = self.model.make_short_sentence(140 - limit)
                full_sentence = "@" + uname + " " + sentence
                print "Responding with: " + full_sentence
                if (not self.dummy):
                   self.responses.append(tweet.id)  
                   self.api.update_status(full_sentence,tweet.id) 
        return
    def target_tweet(self):
        print "Target who? "
        target = raw_input()
        sentence = self.model.make_short_sentence(140 - (len(target) + 2))
        full_sentence = "@"+target+" " + sentence
        print "Tweeting: " + full_sentence
        if (not self.dummy):
            self.api.update_status(full_sentence)

    def save_responses(self):
        with open("responded.txt",'wb') as fp:
            pickle.dump(self.responses,fp)

    def main_loop(self):
        while 1:
            sys.stdout.write('> ')
            cmd = raw_input()
            if cmd == "tweet":
                self.new_tweet()
            if cmd == "respond":
                self.respond_to_tweet()
            if cmd == "current_rate":
                json_rate = self.api.rate_limit_status()
                print json.dumps(json_rate, indent=2)
            if cmd == "target":
                self.target_tweet()
            if cmd == "toggle_dummy":
                if self.dummy == True:
                    self.dummy = False
                    print "No longer in dummy mode"
                else:
                    self.dummy = True
                    print "Now in dummy mode"
            if cmd == "exit":
                self.save_responses()
                return    
