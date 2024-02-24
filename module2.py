import pandas as pd
import networkx as nx

df = pd.read_csv('Top 500 Songs.csv', encoding='latin1')

producer_song_map = {}
producer_collaboration_map = {}

G = nx.Graph()

for _, row in df.iterrows():
    producers = row['producer'].split(', ')
    
    for producer in producers:
        if producer not in producer_song_map:
            producer_song_map[producer] = set()
        producer_song_map[producer].add(row['title'])
    
    for i in range(len(producers)):
        for j in range(i + 1, len(producers)):
            producer1 = producers[i]
            producer2 = producers[j]
            
            if (producer1, producer2) in producer_collaboration_map:
                producer_collaboration_map[(producer1, producer2)] += 1
            else:
                producer_collaboration_map[(producer1, producer2)] = 1

    G.add_node(row['title'], artist=row['artist'])

producer_song_df = pd.DataFrame(producer_song_map.items(), columns=['producer', 'songs'])

producer_collaboration_df = pd.DataFrame(list(producer_collaboration_map.items()), columns=['producer_pair', 'collaborations'])
producer_collaboration_df[['producer1', 'producer2']] = pd.DataFrame(producer_collaboration_df['producer_pair'].tolist(), index=producer_collaboration_df.index)
producer_collaboration_df.drop(columns=['producer_pair'], inplace=True)

for _, row in producer_collaboration_df.iterrows():
    producer1 = row['producer1']
    producer2 = row['producer2']
    collaborations = row['collaborations']
    
    G.add_edge(producer1, producer2, weight=collaborations)

nx.write_graphml(G, 'producer_network.graphml')

print(producer_song_df.head())
print(producer_collaboration_df.head())



#finding top 3 nodes
degree_centrality = nx.degree_centrality(G)

sorted_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)

top_nodes = sorted_nodes[:3]

for node in top_nodes:
    print("Producer:", node)
    print("Collaborations:", G.degree[node])
    print("Degree Centrality:", degree_centrality[node])
    print()