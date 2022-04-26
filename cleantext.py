import json
import os

def get_users():
    path = "/Users/emilyyu/Desktop/Exercises/final_project_json"
    tweeters = []
    for file in os.listdir(f"{path}"):
        if file.endswith(".json"):
            tweeters.append(os.path.splitext(file)[0])
    return tweeters

#keys: data (contain all the tweets), meta (tells other information)
#dictionary[0] 1/30 tweets
#dictionary[0]['data'][0] 0-99 100 tweets in a dictionary
#dictionary[0]['data'] data from every dictionary
#(dictionary[0]['data'][0]['text']) Tweet from every dictionary print(dictionary[0]['data'][0]['text'])
def get_user_tweets(user):
    user_tweets = []
    path = "/Users/emilyyu/Desktop/Exercises/final_project_json"
    with open(f"/Users/emilyyu/Desktop/Exercises/final_project_json/{user}.json") as f:
        dictionary = json.load(f)
        for i in range(len(dictionary)):
            if 'data' in dictionary[i]:
                for j in range(len(dictionary[i]['data'])):
                    tweet = dictionary[i]['data'][j]['text']
                    user_tweets.append(tweet)
    return user_tweets

#keys: users, value: list of the users tweets

def get_tweets(user_dictionary):
    tweeters = get_users()
    for user in tweeters:
        tweet_list = get_user_tweets(user)
        user_dictionary[user] = tweet_list
    return user_dictionary

def main():
    #get_users()
    #get_user_tweets('@barackobama.json')   
    user_dictionary = {}
    #get_tweets(user_dictionary)

if __name__ == "__main__":
    main()