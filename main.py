import tweepy
import time
import sys
from keys import gencdamlakitapkeys
from keys import damlayayinevikeys
from keys import mihrabadyayinkeys
from keys import humayunyayinkeys
from keys import edamladigitalkeys

account = "gencdamlalitap"

def get_twitter_api(keys):
    # personal details
    USER_ID = keys['user_id']
    SCREEN_NAME = keys['screen_name']
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']

    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # authentication of access token and secret
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api

def getParameters():
    parameters = sys.argv
    if parameters:
        del parameters[0]
        return parameters
    else:
        return None

def process():

    parameters = getParameters()
    if parameters:
        account = parameters[0]
        if account == "gencdamlakitap":
            api = get_twitter_api(gencdamlakitapkeys)
        elif account == "damlayayinevi":
            api = get_twitter_api(damlayayinevikeys)
        elif account == "mihrabadyayin":
            api = get_twitter_api(mihrabadyayinkeys)
        elif account == "humayunyayin":
            api = get_twitter_api(humayunyayinkeys)
        elif account == "edamladigital":
            api = get_twitter_api(edamladigitalkeys)
        else:
            print("Account not found")
            exit()

        followers = api.get_follower_ids()
        print("Followers", len(followers))

        friends = api.get_friend_ids()
        print("You follow:", len(friends))

        non_friends = [friend for friend in friends if friend not in followers]
        print("Non-follower Friends:", len(non_friends) )

        logfilename = account + "_non_friends.txt"
        logfile = open(logfilename,"a")
        print("Friendship destroy process is started... Please Wait to finish")
        for nonfriend in non_friends:
            user = api.get_user(user_id = nonfriend)
            screen_name = user.screen_name
            logfile.write(str(nonfriend) + "-" + screen_name + "\n")
            api.destroy_friendship(user_id = nonfriend)
        print(len(non_friends),"non-follower friendship destroyed")
        logfile.close()
    else:
        print("Account not found")
        exit()

if __name__ == "__main__":
 process()
