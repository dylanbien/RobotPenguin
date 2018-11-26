#This file was created to test the goToward function in display.py.
import networkx as nx
G = nx.Graph()

mock_grid = list(range(1,92))#1-91

player_loc = 5
bear_loc = 30

#Creates a node for each across each row
G.add_nodes_from([1, 13])
G.add_nodes_from([14, 26])
G.add_nodes_from([27, 39])
G.add_nodes_from([40, 52])
G.add_nodes_from([53, 65])
G.add_nodes_from([66, 78])
G.add_nodes_from([79, 91])

#start of each row
row_starters = (1, 14, 27, 40, 53, 66, 79)

#connects all the nodes with edges
for r in row_starters:
    for x in range(r, (r+12)):
        G.add_edge(x, x+1)

for x in range(1,54,26):
    for j in range(x, x+14):
        G.add_edge(j, j+13)

for x in range(66,79):
    G.add_edge(x, x+13)

#finds shortest path
print(nx.shortest_path(G, source=player_loc, target=bear_loc))