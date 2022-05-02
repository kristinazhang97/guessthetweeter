import json
import os
from wordcloud import WordCloud
import  matplotlib.pylab as plt
import numpy as np
from user_wordcloud import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_sentiment(tweeter_text, user):
    model = SentimentIntensityAnalyzer()
    scores = model.polarity_scores(tweeter_text)
    #print(user)
    #print(model.polarity_scores(tweeter_text))


    '''
    with open('user_sentiment.txt', 'a') as f:
        f.write(user + '\n')
        f.write("positive: " + str(scores['pos']) + '\n')
        f.write("negative: " + str(scores['neg']) + '\n')
        f.write("neutral: " + str(scores['neu']) + '\n')
        f.write('\n')
    '''

    return model.polarity_scores(tweeter_text)
    
    
def graph_sentiment(sentiment_dict, tweeters):
    positive = []
    negative = []
    neutral = []

    for scores in sentiment_dict.values():
        positive.append(scores['pos'])
        negative.append(scores['neg'])
        neutral.append(scores['neu'])

    #fig = plt.figure()
    #ax = fig.add_axes([0,0,1,1])
    #ax.bar(tweeters,positive)

    plt.bar(tweeters,positive)
    plt.title("Positive Emotions of Tweets")
    plt.xlabel("Twitter Users")
    plt.xticks(rotation = 60, fontsize = 5) 
    plt.ylabel("Percentages")
    plt.show()

    plt.bar(tweeters,negative)
    plt.title("Negative Emotions of Tweets")
    plt.xlabel("Twitter Users")
    plt.xticks(rotation = 60, fontsize = 5) 
    plt.ylabel("Percentages")
    plt.show()

    plt.bar(tweeters,neutral)
    plt.title("Neutral Emotions of Tweets")
    plt.xlabel("Twitter Users")
    plt.xticks(rotation = 60, fontsize = 5) 
    plt.ylabel("Percentages")
    plt.show()


def main():
    tweeters = get_users()
    #f = open('user_sentiment.txt', 'w')
    #f.close()

    sentiment_dict = {}
    for tweeter in tweeters: #iterate through list of tweeters
        user_string = ' '.join(user_words(tweeter))
        sentiment = get_sentiment(user_string, tweeter)
        sentiment_dict[tweeter] = sentiment
    #print(sentiment_dict)
    graph_sentiment(sentiment_dict, tweeters)

    
    
if __name__ == "__main__":
    main()