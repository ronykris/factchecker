import tweepy
from dotenv import load_dotenv
from flask import Flask, request
import os
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)

auth = tweepy.OAuthHandler(os.getenv('consumer_key'), os.getenv('consumer_secret'))
auth.set_access_token(os.getenv('access_token'), os.getenv('access_token_secret'))
api = tweepy.API(auth)

"""
    Function to retrieve details of a source tweet given its unique identifier.

    Args:
        tweetid (int): The unique identifier of the tweet.

    Returns:
        dict: A dictionary containing the following details of the tweet:
            - 'text': The full text of the tweet.
            - 'id': The unique identifier of the tweet.
            - 'user': The screen name of the user who posted the tweet.
            - 'created_at': The date and time at which the tweet was created.

    Raises:
        tweepy.TweepError: If there is an error accessing the Twitter API.

    Examples:
        >>> tweet_id = 123456789
        >>> tweet_details = getSrcTweetDetails(tweet_id)
        >>> print(tweet_details)
        {'text': 'This is the full text of the tweet', 'id': 123456789,
        'user': 'example_user', 'created_at': datetime.datetime(2023, 3, 13, 10, 30, 0)}
    """

def getSrcTweetDetails(tweetid):
    """
    Retrieve details of a source tweet given its unique identifier.

    """
    # Get the tweet details using the Tweepy library.

    tweet = api.get_status(tweetid, tweet_mode="extended")

    
    # Store the tweet details in a dictionary.
    srctweet = {}
    srctweet['text'] = tweet.full_text
    srctweet['id'] = tweet.id
    srctweet['user'] = tweet.user.screen_name
    srctweet['created_at'] = tweet.created_at

    print(srctweet)

    # Return the tweet details as a dictionary.
    return srctweet



def save_dict_to_jsonl(dict_to_save, file_path):
    with open(file_path, 'a') as outfile:
        json.dump(dict_to_save, outfile)
        outfile.write('\n')

def getUserTimeline(screename):
    tweets = api.user_timeline(screen_name=screename, 
        # 200 is the maximum allowed count
        count=300,
        include_rts = False,
        tweet_mode = 'extended' #for full text
    )
    dataarray = []
    for tweet in tweets:
        dataset = {}
        dataset['text'] = tweet.full_text
        dataset['user'] = tweet.user.screen_name
        dataset['id'] = tweet.id
        dataset['created_at'] = str(tweet.created_at)
        dataarray.append(dataset)
        save_dict_to_jsonl(dataset, f'./data_{tweet.user.screen_name}.jsonl')
    print(f'Tweets retruned : {str(len(tweets))}')
    return dataarray


@app.get('/tweets')
def getTweets():
    args = request.args
    url = args.get('tweet')
    tweetID = url.split('/')[-1]
    #url.split('/')[-1].split('?')[0]
    user = getSrcTweetDetails(tweetID)['user']  
    return getUserTimeline(user)

    