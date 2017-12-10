import json
import os
from pprint import pprint

import pandas

from pagerank2 import powerIteration

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

# ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "ENTER YOUR ACCESS TOKEN")
# ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET", "ENTER YOUR ACCESS TOKEN SECRET")
# CONSUMER_KEY = os.environ.get("CONSUMER_KEY", "ENTER YOUR API KEY")
# CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET", "ENTER YOUR API SECRET")
MAX_TWEETS = 3000

# auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
# auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# api = API(auth)

if __name__ == '__main__':
    with open(os.path.join(BASE_DIR, 'tweets.json')) as f:
        tweets_by_user = {}
        tweet_ids = []
        users_rted = {}
        print('Processing tweets...')
        for line in f:
            tweet = json.loads(line)
            if tweet.get('retweetCount', 0) == 0:
                continue
            tweet_id = tweet['object']['id'].split(':')[2]
            actor_id = tweet['object']['actor']['id'].split(':')[2]
            rt_tweet_id = tweet['id'].split(':')[2]
            rt_actor_id = tweet['actor']['id'].split(':')[2]
            if tweet_id not in tweet_ids:
                tweet_ids.append(tweet_id)
            if rt_tweet_id != tweet_id and rt_actor_id != actor_id:
                tweet_rts = users_rted.get(tweet_id, [])
                if rt_actor_id not in tweet_rts:
                    tweet_rts.append(rt_actor_id)
                    users_rted[tweet_id] = tweet_rts
                tweets_actor = tweets_by_user.get(actor_id, [])
                if tweet_id not in tweets_actor:
                    tweets_actor.append(tweet_id)
                    tweets_by_user[actor_id] = tweets_actor

            if len(tweet_ids) > MAX_TWEETS:
                pass
        n = len(tweet_ids)

        print('Processing tweets...done. %d found' % n)
        graph = pandas.DataFrame(index=tweet_ids, columns=tweet_ids, dtype=int)
        print graph
        print('Building graph...')
        for tweet_id in tweet_ids:
            rts = users_rted.get(tweet_id, [])
            for user in rts:
                user_tweets = tweets_by_user.get(user, [])
                for user_tweet in user_tweets:
                    graph[tweet_id][user_tweet] = 1
        print('Building graph...done')

        print('Running TweetRank...')
        rank = powerIteration(graph).sort_values(ascending=False)
        print('Running TweetRank...done')
        pprint(rank[:20])
