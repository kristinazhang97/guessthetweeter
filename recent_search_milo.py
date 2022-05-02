# code taken from Twitter's example code GitHub
# https://github.com/twitterdev/Twitter-API-v2-sample-code


import requests
import os
import json


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


# dictionary of most popular twitter accounts
most_popular_tweeters = {813286 : "@barackobama", 27260086 : "@justinbieber", 21447363 : "@katyperry", 
    79293791 : "@rihanna", 14230524 : "@ladygaga", 44196397 : "@elonmusk", 15846407 : "@theellenshow", 
    10228272 : "@youtube", 25365536 : "@kimkardashian", 23375688 : "@selenagomez", 428333 : "@cnnbrk", 
    783214 : "@twitter", 759251 : "@cnn", 16409683 : "@britneyspears", 11348282 : "@nasa", 21111883 : "@ddlovato", # 16
    807095 : "@nytimes", 15485441 : "@jimmyfallon", 23083404 : "@kingjames", 5402612 : "@bbcbreaking", # 20
    268414482 : "@mileycyrus", 105119490 : "@niallofficial", 96951800 : "@fcbarcelona", 627673190 : "@championsleague", 
    26257166 : "@sportscenter"}

transpose_tweeters = {813286 : 0, 27260086 : 1, 21447363 : 2, 
    79293791 : 3, 14230524 : 4, 44196397 : 5, 15846407 : 6, 
    10228272 : 7, 25365536 : 8, 23375688 : 9, 428333 : 10, 
    783214 : 11, 759251 : 12, 16409683 : 13, 11348282 : 14, 21111883 : 15, # 16
    807095 : 16, 15485441 : 17, 23083404 : 18, 5402612 : 19, # 20
    268414482 : 20, 105119490 : 21, 96951800 : 22, 627673190 : 23, 
    26257166 : 24}


reverse_transpose_tweeters = {0: 813286, 1: 27260086, 2: 21447363, 
    3:79293791, 4:14230524, 5:44196397, 6:15846407, 
    7:10228272, 8:25365536, 9:23375688, 10:428333, 
    11:783214, 12:759251, 13:16409683, 14:11348282, 15:21111883, # 16
    16:807095, 17:15485441, 18:23083404, 19:5402612, # 20
    20:268414482, 21:105119490, 22:96951800, 23:627673190, 
    24:26257166}


def create_url(user_id):
    # if timeline:
    #     endpoint_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    # else:
    endpoint_url = "https://api.twitter.com/2/users/{}/tweets"

    return endpoint_url.format(user_id)


def get_params(pagination_token: str):
    

    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    if pagination_token == "":
        # if timeline:
        #     return {"user_id": f"{user_id}", "since_id": f"{pagination_token}", "count": 200, "include_rts": "false"}
        # else:
        return {"tweet.fields": "created_at", "max_results": 100, "exclude": "retweets"}
    else:
        return {"tweet.fields": "created_at", "max_results": 100, "exclude": "retweets", "pagination_token": f"{pagination_token}"}
    # ["created_at","organic_metrics","geo"]
    # "created_at,organic_metrics,geo"

    # will have to use the until_id to stagger separate requests in order to piece together 3200-point datasets
    # 32 100-tweet requests, updating the until_id each time

    # keep track of the last twitter id so I can use the before field to query them 100 at a time
    # helper functions to break it down step by step
    # separate json files that will all be query-d to build our big ol dataset


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_next_token(json_list: list) -> str:
    # stores and returns the next token from the previous page of results
    # querys the list to get the pagination token from the end, and returns it
    # if list is empty, returns an empty string

    if len(json_list) == 0:
        return ""

    # get the next_token from the last item in the list
    next_token = json_list[-1]['meta']['next_token']

    # return the next_token
    return next_token


def get_json_list(user_id: int, iterations: int):
    # takes a user id as an int and iterations as an int
    # loops through n 100-result iterations, creating a list of json breakdowns
    # returns the list of json dicts

    user_list = []

    for i in range(iterations):
        # create the request url
        url = create_url(user_id)

        # get the next token
        nt = ""
        try:
            nt = get_next_token(user_list)
        except KeyError:
            break

        # create a paramaters object
        params = get_params(pagination_token=nt)
        # collect the java response
        json_response = connect_to_endpoint(url, params)
        # add the json_response to the user_list
        user_list.append(json_response)

    # return the user list
    return user_list

    
def main():

    # create a list of dictionary keys
    dict_list = list(most_popular_tweeters.keys())
    # dict_list = [44196397]


    # for each popular tweeter
    for tweeter in dict_list:
        print(f"{tweeter} : {most_popular_tweeters[tweeter]}")

        # get the tweets list for the tweeter
        tweets_list = get_json_list(user_id=tweeter, iterations=30)

        # print the json response
        # print(json.dumps(json_response, indent=4, sort_keys=True))

        # create a json file
        with open(f'final_project_json/{most_popular_tweeters[tweeter]}.json', 'a') as outfile:
            json.dump(tweets_list, outfile)


if __name__ == "__main__":
    main()