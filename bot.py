#!/usr/bin/python

import tweepy
import markovify
import sys
import threading
import os
import datetime
from keys import keys
from autoresponder import AutoResponder

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
    dbfile = open("/usr/local/autoresponder/tweetdb")
    db = dbfile.read()
    model = markovify.NewlineText(db)
    return model 

def main():
    print "Starting bot"
    api = init_twitter()
    model = init_model()
    accountname = keys['accountname']
    print "loaded settings"
    bot = AutoResponder(model,api, False, "/usr/local/autoresponder/imagedb", accountname)
    print "loaded bot"
    bot.respond_to_tweet()
    now = datetime.datetime.now()
    if now.hour % 2 == 0:
        bot.new_tweet()
    bot.save_responses()

if __name__ == "__main__":
    main()
