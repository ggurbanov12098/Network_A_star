# pip install networkx
# pip install plotly

import networkx
from plotly.graph_objs.scatter.marker import Line
from plotly.graph_objs import *
from plotly.offline import iplot

map_15_dict = {
    0: {'location': (0.0, 0.5), 'link': [1, 2, 3]}, 
    1: {'location': (0.1, 0.7), 'link': [0, 4, 5, 6]}, 
    2: {'location': (0.1, 0.6), 'link': [0, 4, 5, 6]}, 
    3: {'location': (0.1, 0.4), 'link': [0, 4, 5, 6]}, 
    4: {'location': (0.2, 0.6), 'link': [1, 2, 3, 7]}, 
    5: {'location': (0.2, 0.4), 'link': [1, 2, 3, 7, 8, 9]}, 
    6: {'location': (0.2, 0.9), 'link': [1, 2, 3, 8]}, 
    7: {'location': (0.3, 0.7), 'link': [4, 5, 9, 10]}, 
    8: {'location': (0.3, 0.3), 'link': [5, 6, 9, 12]}, 
    9: {'location': (0.4, 0.5), 'link': [5, 7, 8, 10, 11, 12]},
    10: {'location': (0.5, 0.6), 'link': [7, 9, 13]},
    11: {'location': (0.5, 0.5), 'link': [9, 13, 14]},
    12: {'location': (0.5, 0.2), 'link': [8, 9, 14]},
    13: {'location': (0.6, 0.7), 'link': [10, 11]},
    14: {'location': (0.9, 0.4), 'link': [11, 12]}
}


class Map:
    def __init__(self, GraphX):
        self._graph = GraphX
        self.convergence = networkx.get_node_attributes(GraphX, "location")
        self.ways = [list(GraphX[node]) for node in GraphX.nodes()]
        #EXPERIMENTAL
        # self.gScore = 1000
        # self.hScore = 1000
        return
    # def gScore_setter(x):
    #     Map.gScore = x
    #     return Map.gScore
    # def hScore_setter(x):
    #     Map.hScore = x
    #     return Map.hScore

# Map.gScore = None
# Map.hScore = None

def load_map(map_15_dict):
    GraphX = networkx.Graph()
    for node in map_15_dict.keys():
        GraphX.add_node(node, location=map_15_dict[node]['location'])
    for node in map_15_dict.keys():
        for con_node in map_15_dict[node]['link']:
            GraphX.add_edge(node, con_node)
    return Map(GraphX)

def show_map(MapX, start=None, goal=None, path=None):
    GraphX = MapX._graph
    connection_trace = Scatter(
        x=[],
        y=[],
        line=Line(width=2,color='#888'),
	)

    for edge in GraphX.edges():
        x0, y0 = GraphX.nodes[edge[0]]['location']
        x1, y1 = GraphX.nodes[edge[1]]['location']
        connection_trace['x'] += (x0, x1, None)
        connection_trace['y'] += (y0, y1, None)

    router_trace = Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',                                     # parameters = [markers, text]
        hoverinfo='x+y+text',                               # hover style of name of the node 
        marker=Marker(
            showscale=True, 								# Showing scale with colors (Which helps to showcase f(H))
            colorscale='Hot',                               #changes Color Theme
            reversescale=True, 
            color=[],
            size=20, 										# size of nodes
            line=dict(width=4)))  							# Width of node borders (grey circles)
    for node in GraphX.nodes():
        x, y = GraphX.nodes[node]['location']
        router_trace['x'] += (x,)
        router_trace['y'] += (y,)
    
    # assigning colors based on type of node
    for node, adjacencies in enumerate(GraphX.adjacency()):
        color = 0
        if path and node in path:
            color = 2
        if node == start:
            color = 3
        elif node == goal:
            color = 1
        
        router_trace['marker']['color'] += (color,)				                        # Node_trace[marker[color]]
        router_trace['text'] += ("Router " + str(node),)
        # router_trace['text'] += ("Router " + str(node) + "\n preFinal_gScore: " + str(Map.gScore) + " \n preFinal_hScore: " + str(Map.hScore),)

    NetTopology = Figure(data=Data([connection_trace, router_trace]),
                layout=Layout(
                	title='Network Topology using A* search for fast Packet Routing',	# Title name for iplot
                    titlefont=dict(size=20),						                    # Size of font for Title 
                    showlegend=False,								                    # label meanings in Legend
                    hovermode='closest',	# showing labels based on cursor locationtion. Parameters: ['x', 'y', 'closest', False, 'x unified', 'y unified']
                    margin=dict(t=35, b=25, l=7, r=7),					                # margin of grey background border
				 ))
    iplot(NetTopology)
