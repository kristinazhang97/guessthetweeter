import json
import os
from tqdm import tqdm
from wordcloud import WordCloud
import  matplotlib.pylab as plt
import numpy

def get_users():
    path = "/Users/emilyyu/Desktop/Exercises/final_project_json"
    tweeters = []
    for file in os.listdir(f"{path}"):
        if file.endswith(".json"):
            tweeters.append(os.path.splitext(file)[0])
    return tweeters

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

def create_wordcloud(user):
    '''
    #wc  = WordCloud(background_color = "white", mask = mask, max_words=200, stopwords=stopwords)

    wc = WordCloud(max_font_size=40).generate(user)
    wc.generate(text)
    wc.to_file("/Users/emilyyu/Desktop/Exercises/guessthetweeter/tweeter_dictionary.json/fc_barca.png")

    '''
    wc = WordCloud(max_font_size=40).generate(user)

    
    plt.figure(figsize=(20, 8))
    plt.title(user)
    plt.subplot(1, 3, 1)
    plt.imshow(wc, interpolation="bilinear")
    plt.show()

def main():
    print("in beginning of method")
    tweeters=get_users()

    wordlist = []
    fcbarcelona= user_words('@fcbarcelona')
    wordlist.append(fcbarcelona)
    elonmusk= user_words('@elonmusk')
    wordlist.append(elonmusk)
    mileycyrus= user_words('@mileycyrus')
    wordlist.append(mileycyrus)
    britneyspears= user_words('@britneyspears')
    wordlist.append(britneyspears)
    ladygaga= user_words('@ladygaga')
    wordlist.append(ladygaga)
    championsleague= user_words('@championsleague')
    wordlist.append(championsleague)
    youtube= user_words('@youtube')
    wordlist.append(youtube)
    kimkardashian= user_words('@kimkardashian')
    wordlist.append(kimkardashian)
    cnn= user_words('@cnn')
    wordlist.append(cnn)
    ddlovato= user_words('@ddlovato')
    wordlist.append(ddlovato)
    sportscenter= user_words('@sportscenter')
    wordlist.append(sportscenter)
    barackobama= user_words( '@barackobama')
    wordlist.append(barackobama)
    selenagomez= user_words('@selenagomez')
    wordlist.append(selenagomez)
    nasa= user_words('@nasa')
    wordlist.append(nasa)
    jimmyfallon= user_words('@jimmyfallon')
    wordlist.append(jimmyfallon)
    theellenshow= user_words('@theellenshow')
    wordlist.append(theellenshow)
    rihanna= user_words('@rihanna')
    wordlist.append(rihanna)
    bbcbreaking= user_words('@bbcbreaking')
    wordlist.append(bbcbreaking)
    twitter= user_words('@twitter')
    wordlist.append(twitter)
    cnnbrk= user_words('@cnnbrk')
    wordlist.append(cnnbrk)
    kingjames= user_words('@kingjames')
    wordlist.append(kingjames)
    justinbieber= user_words('@justinbieber')
    wordlist.append(justinbieber)
    nytimes= user_words('@nytimes')
    wordlist.append(nytimes)
    niallofficial= user_words('@niallofficial')
    wordlist.append(niallofficial)
    katyperry= user_words('@katyperry')
    wordlist.append(katyperry)

    #print(wordlist[0])
    fc_barca_string = ""
    for word in wordlist[0]:
        fc_barca_string += word + " "
    #print(fc_barca_string)


    create_wordcloud(fc_barca_string)

if __name__ == "__main__":
    main()