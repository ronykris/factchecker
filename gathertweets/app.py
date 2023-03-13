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


"""
Function to retrieve the timeline of a Twitter user and save it to a JSON Lines file.

Args:
    screename (str): The screen name of the Twitter user whose timeline is to be retrieved.

Returns:
    A list of dictionaries containing the details of each tweet in the user's timeline.

Examples:
    >>> user_timeline = getUserTimeline('elonmusk')
"""

def getUserTimeline(screename):
    """
    Retrieve the timeline of a Twitter user and save it to a JSON Lines file.

    The function uses the Twitter API to retrieve the most recent 300 tweets from the specified user's timeline,
    and saves each tweet's details (text, user, id, and created_at) to a JSON Lines file with the user's screen name in the filename.

    Args:
        screename (str): The screen name of the Twitter user whose timeline is to be retrieved.

    Returns:
        A list of dictionaries containing the details of each tweet in the user's timeline.

    Raises:
        tweepy.TweepError: If there is an error connecting to the Twitter API or retrieving the user's timeline.
        IOError: If there is an error writing to the JSON Lines file.
    """

    # Retrieve the most recent 300 tweets from the user's timeline.
    tweets = api.user_timeline(screen_name=screename, 
        # 200 is the maximum allowed count
        count=300,
        include_rts = False,
        tweet_mode = 'extended' #for full text
    )

    # Initialize an empty list to store the tweet details.
    dataarray = []

    # Iterate over each tweet and extract its details.
    for tweet in tweets:
        dataset = {}
        dataset['text'] = tweet.full_text
        dataset['user'] = tweet.user.screen_name
        dataset['id'] = tweet.id
        dataset['created_at'] = str(tweet.created_at)
        dataarray.append(dataset)

        # Save the tweet details to a JSON Lines file with the user's screen name in the filename.
        save_dict_to_jsonl(dataset, f'./data_{tweet.user.screen_name}.jsonl')
    
    # Print the number of tweets retrieved.
    print(f'Tweets retruned : {str(len(tweets))}')

    # Return the list of tweet details.
    return dataarray


@app.get('/tweets')
def getTweets():
    args = request.args
    url = args.get('tweet')
    if url is None:
        raise KeyError('tweet URL not provided as query parameter')
    
    tweetID = url.split('/')[-1]
    #url.split('/')[-1].split('?')[0]
    user = getSrcTweetDetails(tweetID)['user']  
    return getUserTimeline(user)

    