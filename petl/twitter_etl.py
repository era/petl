from TwitterAPI import TwitterAPI
from configparser import ConfigParser
from datetime import datetime
import os

import petl.decorator as petl

config_object = ConfigParser()

config_object.read(os.environ["CONFIG"])


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
    USER_ID = config_object["TWITTER"]["USER_ID"]
    followers = client().request(f"users/:{USER_ID}/followers")

    today = datetime.today().strftime("%Y-%m-%d")

    output = []
    for f in followers:
        output.append([f["id"], today])

    return output

@petl.append("twitter_likes", ["user_id", "updated"], 'updated')
def likes(**kwargs):
    pass

@petl.append("twitter_tweets", ["user_id", "updated"], 'updated')
def tweets(**kwargs):
    pass

if __name__ == "__main__":
    print("Saving followers")
    followers()
    print("Saving followers done")
