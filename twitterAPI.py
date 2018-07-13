

from TwitterAPI import TwitterAPI

Consumer_Key =	'tRI9XJBCMFF9TbU0OzID3ORLo'
Consumer_Secret =	'0jayfDWQQgV65MD5nfoSxBSjHV08OC5TDGvjWtEv8omfX0Zywp'

Access_Token	='1017683083993071617-83VQvXS2KbKmI7ib93JnzqV3KyMFJD'
Access_Secret ='ocqtdzOQJ5lsG6kFn4LphWwHxmiTpk06bl8Sz0PSY72C0'


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