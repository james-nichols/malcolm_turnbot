import os
import time

from markovbot import MarkovBot

# # # # #
# INITIALISE

# Initialise a MarkovBot instance
tweetbot = MarkovBot()

# Get the current directory's path, find Malcolm's speech collections and read it
dirname = os.path.dirname(os.path.abspath(__file__))
book = os.path.join(dirname, u'speeches/all_speeches.txt')
tweetbot.read(book)

# # # # #
# TWUTT

# The MarkovBot uses @sixohsix' Python Twitter Tools, which is a Python wrapper
# for the Twitter API. Find it on GitHub: https://github.com/sixohsix/twitter

cons_key = MY_CONSUMER_KEY 
cons_secret = MY_CONSUMER_SECRET
access_token = MY_ACCESS_TOKEN_KEY
access_token_secret = MY_ACCESS_TOKEN_SECRET

# Log in to Twitter
tweetbot.twitter_login(cons_key, cons_secret, access_token, access_token_secret)

# The target string is what the bot will reply to on Twitter. To learn more,
# read: https://dev.twitter.com/streaming/overview/request-parameters#track
targetstring = 'HeyTurnbot'
keywords = ['disruption', 'agility', 'innovation', 'jobs', 'growth']
prefix = None
suffix = '#ausvotes #TurnbotSpeaks'
maxconvdepth = 5 

tweetbot.twitter_autoreply_start(targetstring, keywords=keywords, prefix=prefix, suffix=suffix, maxconvdepth=maxconvdepth)
tweetbot.twitter_tweeting_start(days=0, hours=1, minutes=0, keywords=None, prefix=None, suffix='#ausvotes')

# Now we wait while the threads do their job
secsinyear = 1 * 365 * 24 * 60 * 60
time.sleep(secsinyear)
 
#tweetbot.twitter_autoreply_stop()
#tweetbot.twitter_tweeting_stop()
