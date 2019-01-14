#This file was created to test the goToward function in display.py.
import networkx as nx
G = nx.Graph()
G.add_nodes_from((1,49))

rows = [list(range(1,8)), list(range(8,15)), list(range(15,22)), list(range(22,29)), list(range(29,36)), list(range(36,43)),list(range(43,50))]
row_pairs = []
for r in rows:
    for x in range(0,len(r)-1):
        row_pairs.append((r[x], r[x+1]))

G.add_edges_from(row_pairs)


print(row_pairs)
coloumn_pairs = []

for c in range(1,8):
    coloumn = list(range(c,43+c,7))
    for x in range(0,len(coloumn)-1):
        coloumn_pairs.append((coloumn[x], coloumn[x+1]))

G.add_edges_from(coloumn_pairs)

print(coloumn_pairs)
print("Test: Finding shortest path from 1 to 29 -  " + str(nx.shortest_path(G, source=1, target=16)))