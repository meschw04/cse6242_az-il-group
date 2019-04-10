import networkx as nx
#import csv
import pandas as pd
import ast

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, WheelZoomTool, PanTool, ResetTool, CustomJS, TapTool
from bokeh.models.graphs import from_networkx
from bokeh.palettes import Spectral4
from bokeh.models.widgets import Select

# TODO: Complete this list
# Add genre selection drop down
# Select the first node
# Select the second node
# Highlight the paths between the two nodes
# Run the VAE on the two nodes and display the new image
# Make Tool Tip look better with some formatting

album_csv = 'large_test.csv'
width = 1200
height = 600
node_size = 8
output_file_name = "interactive_graphs.html"

G = nx.Graph()

with open(album_csv) as csvfile:
    df = pd.read_csv(album_csv)
csvfile.close()

df2 = pd.DataFrame()
df2['AlbumID'] = df['Artist'] + "-- " + df['AlbumName']

scanned_albums = df2['AlbumID'].tolist()
album_pairs = []
genre_tags = [""]

# add nodes
for a, b, c, d, e in zip(df['AlbumName'], df['Artist'], df['Tags'], df['SimilarAlbums'], df['ImageLink']):
    taglist = []
    taglist += ast.literal_eval(c)

    if len(taglist) == 0:
        G.add_node(b + "-- " + a, AlbumName=a, Artist=b, Genre="", Img=e)
    elif taglist[0] != 'albums I own':
        G.add_node(b + "-- " + a, AlbumName=a, Artist=b, Genre=taglist[0], Img=e)
        if taglist[0] not in genre_tags:
            genre_tags.append(taglist[0])
    else:
        G.add_node(b + "-- " + a, AlbumName=a, Artist=b, Genre=taglist[1], Img=e)
        if taglist[0] not in genre_tags:
            genre_tags.append(taglist[1])

    simlist = []
    simlist += ast.literal_eval(d)
    for q in simlist:
        if q[0] + "-- " + q[1] in scanned_albums:
            album_pairs.append([b + "-- " + a, q[0] + "-- " + q[1]])

G.add_edges_from(album_pairs)

plot = Plot(plot_width=width, plot_height=height,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Album Graph Interaction Demonstration: " + str(len(G.node)) + " nodes"

tips = """
    <div>
        <div>
            <img
                src="@Img" height="168" alt="@Img" width="168"
                style="float: left; margin: 0px 15px 15px 0px;"
                border="2"
            ></img>
        </div>
        <div>
            <span style="font-size: 15px;">Album Name:</span>
            <span style="font-size: 15px;">@AlbumName</span>
        </div>
        <div>
            <span style="font-size: 15px;">Artist:</span>
            <span style="font-size: 15px;">@Artist</span>
        </div>
        <div>
            <span style="font-size: 15px;">Genre:</span>
            <span style="font-size: 15px;">@Genre</span>
        </div>
    </div>
"""

# genre = Select(title="Genre", value="All", options=genre_tags)
# not working yet

graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))

callback = CustomJS(args=dict(source=graph_renderer.node_renderer.data_source), code=
    """
    console.log(cb_data.source)
    var inds = cb_data.source.selected['1d'].indices;
    var artist = cb_data.source.data.Img[inds]
    window.alert(artist);
    """)

node_hover_tool = HoverTool(tooltips=tips)
node_select_tool = TapTool(callback=callback)
plot.add_tools(node_hover_tool, WheelZoomTool(), PanTool(), ResetTool(), node_select_tool)

graph_renderer.node_renderer.glyph = Circle(size=node_size, fill_color=Spectral4[0])
graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=0.6, line_width=1)
plot.renderers.append(graph_renderer)


# def select_tags():
#     genre_val = genre.value
#     selected = G.node
#     if genre_val != "All":
#         selected = selected[selected.Genre.str.contains(genre_val) == True]
#     return selected
#
# def update():
#     pass
# not working yet

output_file(output_file_name)
show(plot)