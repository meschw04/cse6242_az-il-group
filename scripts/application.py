from flask import *
import album_bokeh
from bokeh.embed import components


UPLOAD_FOLDER = '../static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__,template_folder="templates")

@app.route('/', methods=['POST', 'GET'])
def main():
    error = None
    blank_script = """<script type="text/javascript"></script>"""
    blank_div = """<div></div>"""
    if request.method == 'POST':
        if request.form['album'] == "":
            node1 = int(request.form['node1'])
            node2 = int(request.form['node2'])
            return "success"
            # node_list = list(G.nodes.keys())
            # if node2 != -1:
            #     shortest_path = nx.all_pairs_shortest_path(G, node_list[node1], node_list[node2])
            #     path = []
            #     for edge in shortest_path:
            #         path.append(G.edges.index(edge))
            #     return json.dumps(path)
            # else:
            #     return json.dumps([])

        if request.form['album'] not in ['Layla', 'Trains', 'Thriller', 'Trouble Will Find Me']:
            error = 'Sorry, we do not have that album right now'

        else:
            if request.form['album'] == 'Trains':
                result = "https://www.youtube.com/watch?v=0UHwkfhwjsk"
                return render_template('album.html', result=result)
            elif request.form['album'] == 'Layla':
                result = "https://www.youtube.com/watch?v=fX5USg8_1gA"
                return render_template('album.html', result=result)
            else:
                album_id = request.form['artist'] + " - " + request.form['album']
                df_limit = int(request.form['numnodes'])
                plot = album_bokeh.main(seed_album_id=album_id, df_limit=df_limit)
                script, div = components(plot)
                return jsonify({"script": script, "div": div})

    return render_template('index.html', script=blank_script, div=blank_div, error=error)


if __name__ == '__main__':
    app.run(debug=True)
