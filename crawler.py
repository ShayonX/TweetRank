from __future__ import print_function

import json
import os
from pprint import pprint

import plotly.plotly as py
import plotly
plotly.tools.set_credentials_file(username='ShayonX', api_key='L85vuTaKTSO6fgpD2NLe')
from plotly.graph_objs import *

import networkx as nx

import pandas

from pagerank import pagerank
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
        graph = pandas.DataFrame(index=tweet_ids, columns=tweet_ids, dtype=int,)

        print('Building graph...')
        for tweet_id in tweet_ids:
            rts = users_rted.get(tweet_id, [])
            for user in rts:
                user_tweets = tweets_by_user.get(user, [])
                for user_tweet in user_tweets:
                    graph[user_tweet][tweet_id] = 1
        print('Building graph...done')

        print('Running TweetRank...')
        rank = powerIteration(graph).sort_values(ascending=False)
        # rank = pagerank(graph).sort_values(ascending=False)
        print('Running TweetRank...done')
        pprint(rank[:20])

        #=--------------------------------------------------------------------------------
        # Converting panda DataFrame n to numpy array
        graphArray = graph.as_matrix(columns=None)

        # Printing number of connecting edges and the tweets that are connected by this edge

        # count = 0
        # print('Starting scan for adjacent edges...')
        # for i in  range(0,graphArray.shape[0]):
        #     for j in range(0,graphArray.shape[1]):
        #         if (graphArray[i][j] == 1):
        #             print('from tweet %s to %s' % (tweet_ids[i],tweet_ids[j]))
        #             count += 1
        # print ('Number of edges = ', (count))

        #--------------------------------------------------------------------------------

        # Getting node positions

        G = nx.random_geometric_graph(200, 0.125)

        pos = nx.get_node_attributes(G, 'pos')

        dmin = 1
        ncenter = 0
        for n in pos:
            x, y = pos[n]
            d = (x - 0.5) ** 2 + (y - 0.5) ** 2
            if d < dmin:
                ncenter = n
                dmin = d

        p = nx.single_source_shortest_path_length(G, ncenter)

        # Creating Edges

        edge_trace = Scatter(
            x=[],
            y=[],
            line=Line(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in G.edges():
            x0, y0 = G.node[edge[0]]['pos']
            x1, y1 = G.node[edge[1]]['pos']
            edge_trace['x'] += [x0, x1, None]
            edge_trace['y'] += [y0, y1, None]

        node_trace = Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=Marker(
                showscale=True,
                # colorscale options
                # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
                # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
                colorscale='YIGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=2)))

        for node in G.nodes():
            x, y = G.node[node]['pos']
            node_trace['x'].append(x)
            node_trace['y'].append(y)

        # Coloring node points

        for node, adjacencies in enumerate(G.adjacency_list()):
            node_trace['marker']['color'].append(len(adjacencies))
            node_info = '# of connections: ' + str(len(adjacencies))
            node_trace['text'].append(node_info)

        # Creating Network Graph

        fig = Figure(data=Data([edge_trace, node_trace]),
                     layout=Layout(
                         title='<br>Network graph made with Python',
                         titlefont=dict(size=16),
                         showlegend=False,
                         hovermode='closest',
                         margin=dict(b=20, l=5, r=5, t=40),
                         annotations=[dict(
                             text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
                             showarrow=False,
                             xref="paper", yref="paper",
                             x=0.005, y=-0.002)],
                         xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                         yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))

        py.plot(fig)