from __future__ import print_function

import pandas as pd
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import sys
import os
import numpy as np
import predict
from twitterAPI import stream
from twitterAPI import get_influence
import company

def analyze_stock():
	return





model = load_model('model.h5')
model.load_weights("weights.h5")

def analyze_twitter(keyword,count=1000):
	texts,tweets = stream(keyword,count=count)
	influences = [get_influence(tweet) for tweet in tweets]
	influences = influences / np.linalg.norm(influences)
	return np.multiply(influences,(predict.predict(model,texts)))

a = (analyze_twitter(company.apple,count=10))
print(a)




