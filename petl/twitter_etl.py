from TwitterAPI import TwitterAPI
from configparser import ConfigParser
from datetime import datetime
import os

import petl.decorator as petl

config_object = ConfigParser()

config_object.read(os.environ["CONFIG"])

USER_ID = config_object["TWITTER"]["USER_ID"]

def client():
    return TwitterAPI(
        config_object["TWITTER"]["CONSUMER_KEY"],
        config_object["TWITTER"]["CONSUMER_SECRET"],
        config_object["TWITTER"]["ACCESS_TOKEN_KEY"],
        config_object["TWITTER"]["ACCESS_TOKEN_SECRET"],
        api_version="2",
    )


@petl.append("twitter_followers", ["user_id", "updated"])
def followers():
    followers = client().request(f"users/:{USER_ID}/followers")

    today = datetime.today().strftime("%Y-%m-%d")

    output = []
    for f in followers:
        output.append([f["id"], today])

    return output

@petl.append("twitter_likes", ["id", "text"])
def likes(**kwargs):
    likes = client().request(f"users/:{USER_ID}/liked_tweets")

    return [[l['id'], l['text']] for l in likes]

@petl.append("twitter_tweets", ["id", "text"], 'id')
def tweets(**kwargs):
    
    if kwargs[petl.COL_MAX_UPDATED_DATE] != None:
        tweets_response = client().request(f"users/:{USER_ID}/tweets", {'since_id': kwargs[petl.COL_MAX_UPDATED_DATE]})
    else:
        tweets_response = client().request(f"users/:{USER_ID}/tweets")

    return [[l['id'], l['text']] for l in tweets_response]
    


if __name__ == "__main__":
    
    print("Saving followers")
    followers()
    print("Saving followers done")

    print("Saving likes")
    likes()
    print("Saving likes done")

    print("Saving tweets")
    tweets()
    print('Saving tweets done')