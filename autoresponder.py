import sys
import tweepy
import json
import os
import pickle
import threading
import time
import random
from random import randint

class AutoResponder():
    def __init__(self,model,api, dummy, idb_location, accountname):
        self.model = model
        self.api = api
        self.dummy = dummy
        self.name = accountname
        self.auto_mode = False;
        self.idb_location = idb_location
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
                resp_type = randint(0,10) 
                print "Responding with type " + str(resp_type) + ": " + full_sentence
                self.responses.append(tweet.id) 
                if (not self.dummy):
                   image = self.get_image()
                   if (resp_type == 0):
                       media_ids = [self.api.media_upload(image).media_id_string] 
                       self.api.update_status(full_sentence,tweet.id,media_ids=media_ids)
                   elif (resp_type == 1):
                       media_ids = [self.api.media_upload(image).media_id_string] 
                       self.api.update_status("@"+uname,tweet.id,media_ids=media_ids)
                   else:
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
    
    def auto(self):
        print "Auto mode engaged"
        while (self.auto_mode):
            self.new_tweet()
            time.sleep(300)
        print "Auto mode finished"

    def toggle_auto(self):
        if (self.auto_mode):
            print "Turning off auto mode"
            self.auto_mode = False
            return
        self.auto_mode = True
        return
    def toggle_dummy(self):
        if self.dummy == True:
            self.dummy = False
            print "No longer in dummy mode"
        else:
            self.dummy = True
            print "Now in dummy mode"
    def get_image(self):
        res =  random.choice(os.listdir(self.idb_location))
        return self.idb_location + "/" + res
  
