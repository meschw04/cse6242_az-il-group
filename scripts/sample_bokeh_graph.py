import networkx as nx
import csv
import pandas as pd
import ast

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx
from bokeh.palettes import Spectral4


album_csv = 'albums_data.csv'

G2 = nx.Graph()

with open(album_csv) as csvfile2:
    df = pd.read_csv(album_csv)
csvfile2.close()

# add nodes
for a, b, c in zip(df['AlbumName'], df['Artist'], df['tags']):
    rowlist = []
    rowlist += ast.literal_eval(c)
    if rowlist[0] != 'albums I own':
        G2.add_node(b + "-- " + a, AlbumName=a, Artist=b, Genre=rowlist[0])
    else:
        G2.add_node(b + "-- " + a, AlbumName=a, Artist=b, Genre=rowlist[1])

# Add Edges
with open('album_pairs.csv') as csvfile:
    data = [tuple(line) for line in csv.reader(csvfile)]
csvfile.close()

G2.add_edges_from(data)

plot = Plot(plot_width=1000, plot_height=1000,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Album Graph Interaction Demonstration: " + str(len(G2.node)) + " nodes"

node_hover_tool = HoverTool(tooltips=[("Album Name", "@AlbumName"), ("Artist", "@Artist"), ("Genre", "@Genre")])
plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

graph_renderer = from_networkx(G2, nx.spring_layout, scale=1, center=(0, 0))

graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=0.8, line_width=1)
plot.renderers.append(graph_renderer)

output_file("interactive_graphs.html")
show(plot)