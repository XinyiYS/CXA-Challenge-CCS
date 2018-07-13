import sys
from  twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import json



Consumer_Key =	'tRI9XJBCMFF9TbU0OzID3ORLo'
Consumer_Secret =	'0jayfDWQQgV65MD5nfoSxBSjHV08OC5TDGvjWtEv8omfX0Zywp'

Access_Token	='1017683083993071617-83VQvXS2KbKmI7ib93JnzqV3KyMFJD'
Access_Secret ='ocqtdzOQJ5lsG6kFn4LphWwHxmiTpk06bl8Sz0PSY72C0'

# STREAM FUNCTION

oauth = OAuth(Access_Token, Access_Secret, Consumer_Key, Consumer_Secret)

# Initiate the connection to Twitter Streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.sample()

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = 1
for tweet in iterator:
    tweet_count -= 1
    print(help(tweet))
    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print (json.dumps(tweet))  
    
    # The command below will do pretty printing for JSON data, try it out
    # print json.dumps(tweet, indent=4)
       
    if tweet_count <= 0:
        break 



# SEARCH FUNCTION BELOW:



#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(auth = OAuth(Access_Token,
                  Access_Secret,
                  Consumer_Key,
                  Consumer_Secret))

#-----------------------------------------------------------------------
# perform a user search 
# twitter API docs: https://dev.twitter.com/rest/reference/get/users/search
#-----------------------------------------------------------------------
results = twitter.users.search(q = '"google"')


#-----------------------------------------------------------------------
# loop through each of the users, and print their details
#-----------------------------------------------------------------------
for user in results:
    print("@%s (%s): %s" % (user["screen_name"], user["name"], user["location"]))