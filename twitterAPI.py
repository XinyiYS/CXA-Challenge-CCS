from TwitterAPI import TwitterAPI
import config
import preprocessor as p

Consumer_Key =	config.twitter_config['Consumer_Key']
Consumer_Secret =	config.twitter_config['Consumer_Secret']
Access_Token	= config.twitter_config['Access_Token']
Access_Secret = config.twitter_config['Access_Secret']

api = TwitterAPI(Consumer_Key, Consumer_Secret, Access_Token, Access_Secret)

def stream(keyword,count=1000):
	r = api.request('statuses/filter', {'track':keyword})
	texts ,tweets = [],[]
	for item in r.get_iterator():
		if 'text' in item:
			if 'lang' in item and item['lang'] == 'en':
				texts.append(p.clean(item['text'])+"\n")
				tweets.append(item)
				count -= 1
		if count ==0:
			break
	return texts,tweets

def get_influence(tweet):
	influence = 1
	if 'reply_count' in tweet:
		influence += tweet['reply_count']
	if 'retweet_count' in tweet:
		influence += tweet['reply_count']
	if 'favorite_count' in tweet:
		influence += tweet['favorite_count']
	if 'reply_count' in tweet:
		influence += tweet['reply_count']
	return influence


import company
motorola = company.motorola
amazon = company.amazon
apple = company.apple
google = company.google
facebook = company.facebook

if __name__ == '__main__':
	for a in (amazon,apple,google,facebook,motorola):
		with open('tweet_hist.txt','a') as w:
			texts = stream(a,50)[0]
			for text in texts:
				w.write(text)



