import json
import os
import nltk
import string
from text_preprocessing import *

#returns a list of the 25 tweeter users
def get_users():
    path = "/Users/emilyyu/Desktop/Exercises/final_project_json"
    tweeters = []
    for file in os.listdir(f"{path}"):
        if file.endswith(".json"):
            tweeters.append(os.path.splitext(file)[0])
    return tweeters

#returns a list of strings of clean words of the tweet
def clean_tweet(text):
    tweet = remove_URL(text)
    tweet = replace_contractions(tweet)
    words = nltk.word_tokenize(tweet)
    words = normalize(words)
    return words

#returns a list of the users tweets
def get_user_tweets(user):
    user_tweets = []
    path = "/Users/emilyyu/Desktop/Exercises/final_project_json"
    with open(f"/Users/emilyyu/Desktop/Exercises/final_project_json/{user}.json") as f:
        dictionary = json.load(f)
        for i in range(len(dictionary)):
            if 'data' in dictionary[i]:
                for j in range(len(dictionary[i]['data'])):
                    tweet = dictionary[i]['data'][j]['text']
                    tweet = clean_tweet(tweet)
                    user_tweets.append(tweet)
    return user_tweets

#returns a dictionary of keys: tweeter users, value: list of the users tweets
def get_tweets(user_dictionary):
    tweeters = get_users()
    for user in tweeters:
        tweet_list = get_user_tweets(user)
        user_dictionary[user] = tweet_list
    return user_dictionary

def main():
    #get_users()
    print(get_user_tweets('@barackobama')) 
    #print('Tune in at 11:35 a.m. ET to watch the President deliver a commencement speech at the U.S. Coast Guard Academy: http://t.co/0CUMi3p5BU')
    #print(clean_tweet('Tune in at 11:35 a.m. ET to watch the President deliver a commencement speech at the U.S. Coast Guard Academy: http://t.co/0CUMi3p5BU'))  
    #user_dictionary = {}
    #get_tweets(user_dictionary)
    


if __name__ == "__main__":
    main()

#Understanding the JSON
#keys: data (contain all the tweets), meta (tells other information)
#dictionary[0] 1/30 tweets
#dictionary[0]['data'][0] 0-99 100 tweets in a dictionary
#dictionary[0]['data'] data from every dictionary
#(dictionary[0]['data'][0]['text']) Tweet from every dictionary print(dictionary[0]['data'][0]['text'])