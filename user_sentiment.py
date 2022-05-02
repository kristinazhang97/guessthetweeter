import json
import os
from wordcloud import WordCloud
import  matplotlib.pylab as plt
import numpy as np
from user_wordcloud import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_sentiment(tweeter_text, user):
    model = SentimentIntensityAnalyzer()
    user_positive = []
    user_neutral = []
    user_negative = []

    scores = model.polarity_scores(tweeter_text)
    #print(model.polarity_scores(tweeter_text))

    print(user)
    print("negative: ", scores['neg'])
    print("positive: ", scores['pos'])
    print("neutral: ", scores['neu'])
    print()

def main():
    tweeters = get_users()

    for tweeter in tweeters: #iterate through list of tweeters
        user_string = ' '.join(user_words(tweeter))
        get_sentiment(user_string, tweeter)


if __name__ == "__main__":
    main()