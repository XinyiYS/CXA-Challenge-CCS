

from TwitterAPI import TwitterAPI
import config


Consumer_Key =	config.twitter_config['Consumer_Key']
Consumer_Secret =	config.twitter_config['Consumer_Secret']

Access_Token	= config.twitter_config['Access_Token']
Access_Secret = config.twitter_config['Access_Secret']


api = TwitterAPI(Consumer_Key, Consumer_Secret, Access_Token, Access_Secret)

# Tweet something:
# r = api.request('statuses/update', {'status':'This is a tweet!'})
# print(r.status_code)
# Get tweet by its id:

r = api.request('statuses/show/:%d' % 210462857140252672)
print(r.text)

# Get some tweets:

r = api.request('search/tweets', {'q':'pizza'})
for item in r:
        print(item)

# Stream tweets from New York City:

r = api.request('statuses/filter', {'locations':'-74,40,-73,41'})
for item in r:
        print(item)