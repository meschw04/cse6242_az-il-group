
import networkx as nx
import pandas as pd
import ast
import random
import json
# import collections as cl

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, WheelZoomTool, PanTool, ResetTool, CustomJS, \
    TapTool
from bokeh.models.graphs import from_networkx
from bokeh.palettes import Spectral4
from bokeh.models.widgets import Select
from bokeh.layouts import layout, column
from bokeh.io import curdoc


'''
(done)		Using other file, build a connected graph from an input node

(doneish)	Hover window format

		Better graph layout?

		Assign node colors accordign to genre

		Allow building a graph by genre from the smaller dataset

(done)		Have user specified node in red

(still needed?)	Cut off text fields after a certain length to guarantee formatting

		Create a list of acceptable genres (tags)

(done?)		Add a "recenter" option that recreates the bokeh figure using a new node as the seed

(done)		Limit number of similar albums to 5 when generating network

'''


def get_idxs(df, seed_album_id, node_sim_limit, df_limit):
    # This function returns rows from dataframe
    def get_row_data(df, seed, node_sim_limit):
        try:
            rows = df.loc[df['album_id'] == seed]
            row = rows.iloc[0]
            idx = row.name
            similar_albums = ast.literal_eval(row['similar_albums'])
            random.shuffle(similar_albums)
            similar_albums = similar_albums[:node_sim_limit]
            return idx, similar_albums
        except:
            return None

    # Construct dataset
    keep_idxs = []
    seeds = {0: [seed_album_id]}
    while True:

        # Get keys associated with seed dictionary
        seed_keys = sorted(list(seeds.keys()))

        # Break if no more seeds
        seeds_left = sum([len(seeds[k]) for k in seeds])
        if seeds_left == 0:
            break

        # Get current seed
        for seed_key in seed_keys:
            if len(seeds[seed_key]) > 0:
                random.shuffle(seeds[seed_key])
                seed = seeds[seed_key].pop()
                break

        # Get row for seed
        row_data = get_row_data(df, seed, node_sim_limit)
        if row_data is not None:
            (idx, similar_albums) = row_data
        else:
            continue

        # Add index to row
        if idx not in keep_idxs:
            keep_idxs.append(idx)

        # Break if necessary
        if len(keep_idxs) == df_limit:
            break

        # Construct seeds from similar album data
        sim_album_seeds = []
        for (sim_album, sim_artist) in similar_albums:
            sim_album_id = sim_album + ' - ' + sim_artist
            sim_album_seeds.append(sim_album_id)
        seed_key_next = seed_key + 1
        if seed_key_next in seeds:
            seeds[seed_key_next] = seeds[seed_key_next] + sim_album_seeds
        else:
            seeds[seed_key_next] = sim_album_seeds

    # Return determined indices
    return keep_idxs


def generate_graph(album_csv, seed_album_id, node_sim_limit, df_limit, width, height, node_size, output_file_name,
                   show_fig):
    # Read data into a pandas dataframe
    df = pd.read_csv(album_csv, encoding='latin1')

    # Add an album id column to the dataframe for the artist - album pair
    df['album_id'] = df['artist'] + ' - ' + df['album_name']

    # Parse dataframe
    keep_idxs = get_idxs(df, seed_album_id, node_sim_limit, df_limit)
    df = df.loc[keep_idxs]

    # Add nodes to graph
    album_edges = []
    G = nx.Graph()
    scanned_album_ids = df['album_id'].tolist()

    genre_list = set()

    for index, row in df.iterrows():

        # Extract necessary values from row
        album_id = row['album_id']
        node_color = "yellow" if album_id == seed_album_id else "LightSkyBlue"  # Spectral4[0]
        album_name = row['album_name']
        artist = row['artist']
        tags = ast.literal_eval(row['tags'])
        similar_albums = ast.literal_eval(row['similar_albums'])
        image_link = row['image_link']

        # Add nodes to graph
        tags = [t.capitalize() for t in tags if t.lower() not in ['albums i own', artist.lower()]]

        for t in tags:
            genre_list.add(t)

        if len(tags) == 0:
            genre = 'N/A'
        else:
            genre = ', '.join(tags)
        G.add_node(album_id, album_name=album_name, artist=artist, genre=genre, img=image_link, node_color=node_color)

        # Create list of similar albums
        for (sim_album, sim_artist) in similar_albums:
            sim_album_id = sim_album + ' - ' + sim_artist
            if sim_album_id in scanned_album_ids:
                album_edges.append([album_id, sim_album_id])

    # Add edges to graph
    G.add_edges_from(album_edges)

    # Plot the graph
    graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
    graph_renderer.node_renderer.glyph = Circle(size=node_size, fill_color="node_color")
    graph_renderer.node_renderer.nonselection_glyph = Circle(size=node_size, fill_color="node_color")
    graph_renderer.edge_renderer.glyph = MultiLine(line_color="black", line_alpha=0.6, line_width=1)

    plot = Plot(plot_width=width, plot_height=height, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plot.title.text = 'Album Graph Interaction Demonstration: {} nodes'.format(len(G.node))
    tips = """
	    <div id="header" style="width:220px;">
		<div>
		    <img
		        src="@img" height="168px" alt="@img" width="168px"
		        style="float: left; margin: 0px 15px 15px 0px;"
		        border="2"
		    ></img>
		</div>
		<div>
		    <span style="font-size: 15px;"><b>Album Name:</b></span><br>
		    <span style="font-size: 12px;">&nbsp;&nbsp;@album_name</span>
		</div>
		<div>
		    <span style="font-size: 15px;"><b>Artist:</b></span><br>
		    <span style="font-size: 12px;">&nbsp;&nbsp;@artist</span>
		</div>
		<div>
		    <span style="font-size: 15px;"><b>Genre:</b></span><br>
		    <span style="font-size: 12px;">&nbsp;&nbsp;@genre</span>
		</div>
	    </div>
	"""
    node_hover_tool = HoverTool(tooltips=tips)

    callback = CustomJS(args=dict(source=graph_renderer.node_renderer.data_source), code=
    """
    if (window.count == null) {
        window.count = 0
        window.node1 = [-1]
        window.node2 = [-1]
        window.node1_URL = ""
        window.node2_URL = ""
    }
    debugger;
    window.count = window.count + 1
    var inds = cb_data.source.selected['1d'].indices;
    cb_data.source.data.node_color[inds] = "green"
    if (window.count % 2 == 1){
        if (window.node1 == 0) {
            cb_data.source.data.node_color[window.node1] = "yellow"
        } else {cb_data.source.data.node_color[window.node1] = "LightSkyBlue"}
        window.node1 = inds
        window.node1_URL = cb_data.source.data.img[inds]
    } else {
        if (window.node2 == 0) {
            cb_data.source.data.node_color[window.node2] = "yellow"
        } else {cb_data.source.data.node_color[window.node2] = "LightSkyBlue"}
        window.node2 = inds
        window.node2_URL = cb_data.source.data.img[inds]
    }
    $.post( 
        "http://127.0.0.1:5000/", 
        { node1: window.node1[0], node2: window.node2[0], album: "" }
    );
    """)
    # , function (data) {var obj = JSON.parse(data); debugger;}
    # add above back in to $.Post to receive data from flask
    node_select_tool = TapTool(callback=callback)

    callback2 = CustomJS(args=dict(source=graph_renderer.node_renderer.data_source, length=G.number_of_nodes()), code=
    """
    debugger;
    var val = cb_obj.value
    var i;
    for (i = 0; i < length; i++) { 
        if (source.data.node_color[i] != "green"){
            if (source.data.genre[i].includes(val)){
                source.data.node_color[i] = "purple";
            } else {
                if (i==0) {
                    source.data.node_color[i] = "yellow";
                } else {
                    source.data.node_color[i] = "LightSkyBlue";
                }
            }
        }
    }
    """)
    genre_list = list(genre_list)
    genre_list.sort()
    genre = Select(title="Genre", value="All", options=genre_list, callback=callback2)

    plot.add_tools(node_hover_tool, WheelZoomTool(), PanTool(), ResetTool(), node_select_tool)
    plot.renderers.append(graph_renderer)
    output_file(output_file_name)

    controls = [genre]
    inputs = column(*controls, width=320, height=90)
    inputs.sizing_mode = "fixed"
    l = layout([
        [inputs], [plot],
    ], sizing_mode="fixed")

    if show_fig:
        show(l)
    return l, G


def main(seed_album_id='Michael Jackson' + ' - ' + 'Thriller', df_limit=50):
    # Define key variables
    album_csv = 'large_test.csv'
    node_sim_limit = 5
    node_size = 15
    width = 1200
    height = 600
    output_file_name = 'interactive_graphs.html'
    show_fig = False

    # Generate graph
    plot, G = generate_graph(album_csv, seed_album_id, node_sim_limit, df_limit, width, height, node_size, output_file_name,
        show_fig)

    return plot, G


if __name__ == '__main__':
    main()
