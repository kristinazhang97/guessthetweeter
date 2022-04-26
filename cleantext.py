import json
import os


def get_users():
    path = "/Users/emilyyu/Desktop/Exercises/final_project_json"
    tweeters = []
    for file in os.listdir(f"{path}"):
        if file.endswith(".json"):
            tweeters.append(os.path.splitext(file)[0])
    print(tweeters)

#keys: data (contain all the tweets), meta (tells other information)
#dictionary[0] 1/30 tweets
#dictionary[0]['data'][0] 0-99 100 tweets in a dictionary
#dictionary[0]['data'] data from every dictionary
#(dictionary[0]['data'][0]['text']) Tweet from every dictionary print(dictionary[0]['data'][0]['text'])
def get_tweets(user):
    path = "/Users/emilyyu/Desktop/Exercises/final_project_json"
    with open(f"/Users/emilyyu/Desktop/Exercises/final_project_json/{user}") as f:
        dictionary = json.load(f)
        for i in range(len(dictionary)):
            for j in range(len(dictionary[i]['data'])):
                tweet = dictionary[i]['data'][j]['text']
                print(tweet)

def main():
    #get_users()
    get_tweets('@barackobama.json')   

if __name__ == "__main__":
    main()