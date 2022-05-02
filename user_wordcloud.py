import json
import os
from tqdm import tqdm
from wordcloud import WordCloud
import  matplotlib.pylab as plt
import numpy

#returns a list of the 25 twitter users
def get_users():
    path = "/Users/emilyyu/Desktop/Exercises/final_project_json"
    tweeters = []
    for file in os.listdir(f"{path}"):
        if file.endswith(".json"):
            tweeters.append(os.path.splitext(file)[0])
    return tweeters

#Returns a list of all the unique words in the users tweets
def user_words(user):
    user_word= set()
    with open(f"/Users/emilyyu/Desktop/Exercises/guessthetweeter/tweeter_dictionary.json") as f:
        dictionary = json.load(f)
        for user_name in dictionary:
            if user_name == user:
                for tweets in dictionary[user_name]:
                    for word in tweets:
                        user_word.add(word)
    return list(user_word)

#Create word cloud for each user and saving them as a jpg
def create_wordcloud(user, title):
    wc = WordCloud(max_font_size=40).generate(user)

    plt.figure(figsize=(20, 8))
    plt.title(user)
    plt.subplot(1, 3, 1)
    plt.imshow(wc, interpolation="bilinear")
    plt.savefig(f"{title}.jpg")


def main():
    tweeters = get_users()

    for tweeter in tweeters: #iterate through list of tweeters
        user_string = ' '.join(user_words(tweeter))
        create_wordcloud(user_string, tweeter)

if __name__ == "__main__":
    main()