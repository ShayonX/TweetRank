from __future__ import print_function

import json
import os
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import plotly

plotly.tools.set_credentials_file(username='ShayonX', api_key='L85vuTaKTSO6fgpD2NLe')

import networkx as nx

import pandas

from pagerank import pagerank

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, 'results')

MAX_TWEETS = None


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

            if MAX_TWEETS and len(tweet_ids) > MAX_TWEETS:
                break
        n = len(tweet_ids)

        print('Processing tweets...done. %d found' % n)
        graph = pandas.DataFrame(index=tweet_ids, columns=tweet_ids, dtype=int, )

        print('Building graph...')
        for tweet_id in tweet_ids:
            rts = users_rted.get(tweet_id, [])
            for user in rts:
                user_tweets = tweets_by_user.get(user, [])
                for user_tweet in user_tweets:
                    graph[user_tweet][tweet_id] = 1
        print('Building graph...done')

        print('Running TweetRank...')
        # rank = powerIteration(graph).sort_values(ascending=False)
        rank = pagerank(graph).sort_values(ascending=False)

        print('Running TweetRank...done')
        pprint(rank[:10])
        rank.to_csv('ranking.csv')

        # =--------------------------------------------------------------------------------
        # Converting panda DataFrame n to numpy array
        graphArray = graph.as_matrix(columns=None)
        # print(graphArray)

        # Creating Network Graph from adjacency matrix
        rows, cols = np.where(graphArray == 1)
        edges = zip(rows.tolist(), cols.tolist())
        G = nx.DiGraph()
        pos = nx.spring_layout(G)
        G.add_edges_from(edges)
        # labels = {}
        # for i in range(0,len(tweet_ids)):
        #     labels[i]=tweet_ids[i]
        # nx.draw_networkx_labels(G,font_size=7)
        # mylabels = {k: v for k, v in enumerate(tweet_ids)}
        keys = rank.keys()
        mylabels = {i: keys.get_loc(t_id) for i, t_id in enumerate(tweet_ids)}
        nx.draw_random(G, node_size=200, with_labels=True,label=mylabels)
        plt.show()



