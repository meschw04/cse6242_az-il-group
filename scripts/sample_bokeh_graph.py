import networkx as nx
import csv
import pandas as pd
import ast

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx
from bokeh.palettes import Spectral4


album_csv = 'large_test.csv'
width = 2000
height = 1000
node_size = 8
output_file_name = "interactive_graphs.html"

G2 = nx.Graph()

with open(album_csv) as csvfile:
    df = pd.read_csv(album_csv)
csvfile.close()

scanned_albums = df['AlbumName'].tolist()
album_pairs = []

# add nodes
for a, b, c, d in zip(df['AlbumName'], df['Artist'], df['Tags'], df['SimilarAlbums']):
    taglist = []
    taglist += ast.literal_eval(c)

    if len(taglist) == 0:
        G2.add_node(b + "-- " + a, AlbumName=a, Artist=b, Genre="")
    elif taglist[0] != 'albums I own':
        G2.add_node(b + "-- " + a, AlbumName=a, Artist=b, Genre=taglist[0])
    else:
        G2.add_node(b + "-- " + a, AlbumName=a, Artist=b, Genre=taglist[1])

    simlist = []
    simlist += ast.literal_eval(d)
    for q in simlist:
        if q[1] in scanned_albums:
            album_pairs.append([b + "-- " + a, q[0] + "-- " + q[1]])

G2.add_edges_from(album_pairs)

plot = Plot(plot_width=width, plot_height=height,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Album Graph Interaction Demonstration: " + str(len(G2.node)) + " nodes"

node_hover_tool = HoverTool(tooltips=[("Album Name", "@AlbumName"), ("Artist", "@Artist"), ("Genre", "@Genre")])
plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

graph_renderer = from_networkx(G2, nx.spring_layout, scale=1, center=(0, 0))

graph_renderer.node_renderer.glyph = Circle(size=node_size, fill_color=Spectral4[0])
graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=0.8, line_width=1)
plot.renderers.append(graph_renderer)

output_file(output_file_name)
show(plot)