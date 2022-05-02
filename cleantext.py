import json
import os
import nltk
import string
import pandas as pd
import numpy as np
from text_preprocessing import *
from tqdm import tqdm
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from scipy import sparse
# create a inverse map from the id : handle map in recent_search_milo.py
from recent_search_milo import most_popular_tweeters


#returns a list of the 25 tweeter users
def get_users():
    path = "/Users/emilyyu/Desktop/Exercises/final_project_json"
    tweeters = []
    for file in os.listdir(f"{path}"):
        if file.endswith(".json"):
            tweeters.append(os.path.splitext(file)[0])
    return tweeters

#returns a list of strings of clean words of the tweet
def clean_tweet(tweet):

    # split the tweet on spaces
    tweet = tweet.split()

    # remove hashtags and mentions
    tweet = [word for word in tweet if ("#" not in word and "@" not in word)]

    # turn the tweet back into a string
    tweet = " ".join(tweet)

    tweet = remove_URL(tweet)
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
                    if len(tweet) != 0:
                        user_tweets.append(tweet)
    return user_tweets

#returns a dictionary of key: tweeter users, value: list of the users tweets
def get_tweets(user_dictionary):
    tweeters = get_users()
    for user in tqdm(tweeters):
        tweet_list = get_user_tweets(user)
        user_dictionary[user] = tweet_list
    return user_dictionary


def all_words(filepath: str="/Users/emilyyu/Desktop/Exercises/guessthetweeter/tweeter_dictionary.json"):
    all_words = set()
    with open(filepath) as f:
        dictionary = json.load(f)
        #iterating through each user
        for user in dictionary:
            #iterating through each tweet of the user
            for tweets in dictionary[user]:
                #iterating through every word of the tweet
                for word in tweets:
                    all_words.add(word)
    return all_words 

def get_tuples():
    list_tuples = []
    with open(f"/Users/emilyyu/Desktop/Exercises/guessthetweeter/tweeter_dictionary.json") as f:
        dictionary = json.load(f)
        for user in dictionary:
            for tweet in dictionary[user]:
                user_tuple = (user, tweet)
                list_tuples.append(user_tuple)
    return list_tuples

#iterating through the tuples
#creating a list of lists of the frequencies of the words in the tweets

def create_word_matrix(user_tuples, all_words):
    #user_tuples is a list of tuples with (ID, [list of words in tweet])
    user_matrix = []
    for users in tqdm(user_tuples): #iterate through tuples
        tweet_matrix = {} #values 
        tweet = Counter(users[1]) # converts into dictionary where keys are words and values are counts
        for word in all_words:
            tweet_matrix[word] = 0
            if word in tweet:
                tweet_matrix[word] = tweet[word]
        user_matrix.append(list(tweet_matrix.values()))
    return user_matrix #returns a list of lists

#Checking the word matrix to check if the number of 1's matches the length of the tweet
def check_matrix(tuples_list, matrix):
    for i  in range(len(tuples_list)):#iterate through tuples
        status = False
        tweet = tuples_list[i][1] #grab the second index of each tuple
        for num in matrix[i]: #iterate through ith list through each number and count 1
            if (num>1):
                print(tweet, num)
    return status
        

def create_dataframe(all_words, list_tuples):
    data = pd.DataFrame(dictionary.values(), columns = all_words, index = list_tuples)
    #DATA MAKE DICTIONARY 
    #INDEX = LIST OF THE TUPLES
    #print(data)
    #data.to_csv("/Users/emilyyu/Desktop/Exercises/guessthetweeter/tweeter_matrix.csv")



# milo's methods

# gets a list from a user dictionary list file.json
def get_dictionary_from_json(fp: str) -> list:
    '''
    takes a filepath fp
    opens the .json file at filepath fp and returns
    a json object read in from the file
    '''

    # read in the file
    with open(fp) as f:
        # create an object
        json_obj = json.load(f)
        return json_obj


# need a dictonary ---> user_id : list of tweets, parsed and cleaned
def get_user_dict(user_id: int, user_list: list) -> dict:
    '''
    takes a (user_id: int, user_list: list)
    user list is a list of dictionaries
    returns a dict user_id : list of tweets, parsed and cleaned
    '''
    
    # create a new list to hold the cleaned tweets
    tweets = []
    # iterate through user_list
    for dictionary in tqdm(user_list):
        # iterate through the tweets in the dictionary
        # if the dictionary has a data key
        if 'data' in dictionary:
            for tweet in dictionary['data']:
                # get the clean text from the tweet
                text = clean_tweet(tweet['text'])
                # add the text to tweets if it has a length longer than 0
                if len(text) > 0:
                    tweets.append(text)

    # return a dictionary with the user id as the key and the list of parsed clean tweets as the value
    return {user_id : tweets}


# get a full dictionary from all the files in a directory
def get_full_dict(directory_path: str) -> dict:
    # reverse dict is @handle : id
    reverse_dict = {v: k for k, v in most_popular_tweeters.items()}

    # create a full dictionary to be returned
    full_dict = {}

    # get a list of the files in the directory
    dir_list = [user for user in os.listdir(directory_path) if user.endswith('.json')]
    # iterate through dir_list
    for user in tqdm(dir_list):
        # get the user's json list from the file
        raw_list = get_dictionary_from_json(directory_path + user)
        # get a dict of the cleaned tweets from the raw json file
        clean_dict = get_user_dict(reverse_dict[user[:-5]], raw_list)
        # add the clean list to the full dictionary
        full_dict.update(clean_dict)
    
    # return the full dictionary
    return full_dict


# return a list of all the words in a dictionary with values : list of lists of words
def get_word_set(filepath="", filename="milo_json_data.json") -> list:
    # import the tweet data
    # filepath = "/Users/milo/Documents/dis_copenhagen/big_data/guessthetweeter/"
    filepath = ""

    with open(f"{filepath}{filename}") as fp:
        tweet_text_dict = json.load(fp)

    # get a list of the tweets from the dictionary
    tweets_list = list(tweet_text_dict.values())

    # create a flattened list out of the tweet data
    flat_tweets = [word for user in tweets_list for tweet in user for word in tweet]

    # create a dictionary out of flat_tweets with word : frequency
    word_freq_dict = Counter(flat_tweets)

    # create a list out of the word_freq_dict for words with a frequency of over 1
    word_set = [word for word in word_freq_dict.keys() if word_freq_dict[word] > 2]

    return word_set


# return a word vector of word frequency data
def get_word_vector(tweet: list, cv, iden=None):

    # create a word_vector to be returned
    word_vector = cv.fit_transform([" ".join(tweet)])

    # change the word vector to a numpy array
    word_vector = word_vector.toarray()

    if iden != None:
        # add the id to the end of the word_vector
        word_vector = np.append(word_vector, np.array([iden]))
   
    # return the word vector, identity
    return word_vector


# return a list of bag of words style word vectors given a tweeter id and the tweet dict file
def get_tweeter_vectors(iden: int, words_list: list, tweet_file: str="milo_json_data.json"):
    # import the dict from the file
    with open(tweet_file) as fp:
        tweet_dict = json.load(fp)

    # create a CountVectorizer
    cv = CountVectorizer(vocabulary=words_list)

    # get the data for the given id, should be a list of lists
    tweets = tweet_dict[str(iden)]
    tweet_vectors = [get_word_vector(tweet, cv, iden) for tweet in tweets]

    # change the return vector to a numpy array
    tweet_vectors_np = np.array(tweet_vectors, dtype=list)

    # return the master list
    return tweet_vectors_np


def main():
    # words = all_words() #columns
    # tuples_list = get_tuples() #rows
    # test_list = tuples_list[0:1000]
    # matrix = create_word_matrix(test_list, words)
    # print(check_matrix(test_list, matrix))
    # #create_dataframe(all_words, tuples_list, matrix)

    # #Saved to a JSON FILE TO WORK ON EASIER
    # #with open("/Users/emilyyu/Desktop/Exercises/guessthetweeter/tweeter_dictionary.json", "w") as write_file:
    #     #json.dump(user_dictionary, write_file, indent=4)


    ## MILO
    # # get all tweets
    # all_tweets_dict = get_full_dict("/Users/milo/Documents/dis_copenhagen/big_data/final_project_json/")
    # # dump them to a json file
    # with open('milo_json_data.json', 'w') as outfile:
    #     json.dump(all_tweets_dict, outfile)

    pass

    
if __name__ == "__main__":
    main()

#Understanding the JSON
#keys: data (contain all the tweets), meta (tells other information)
#dictionary[0] 1/30 tweets
#dictionary[0]['data'][0] 0-99 100 tweets in a dictionary
#dictionary[0]['data'] data from every dictionary
#(dictionary[0]['data'][0]['text']) Tweet from every dictionary print(dictionary[0]['data'][0]['text'])