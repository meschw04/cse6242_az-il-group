from flask import *
from flask_cors import CORS
import album_bokeh
import run_autoencoder
from bokeh.embed import components


UPLOAD_FOLDER = '../static'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__,template_folder="templates")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
CORS(app)

@app.route('/', methods=['POST', 'GET'])
def main():
    error = None
    blank_script = """<script type="text/javascript"></script>"""
    blank_div = """<div></div>"""
    if request.method == 'POST':
        if request.form['album'] == "run_ae":
            node1_URL = request.form['node1_URL']
            node2_URL = request.form['node2_URL']
            run_autoencoder.run_autoencoder(node1_URL, node2_URL)
            return "success"

        else:
            album_id = request.form['artist'] + " - " + request.form['album']
            df_limit = int(request.form['numnodes'])
            plot, suggestion = album_bokeh.main(seed_album_id=album_id, df_limit=df_limit)
            if suggestion == None:
                suggestion = ""
                script, div = components(plot)
            else:
                script = ""
                div = ""
            return jsonify({"script": script, "div": div, "suggestion": suggestion})

    return render_template('index.html', script=blank_script, div=blank_div, error=error)

@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    app.run(debug=True)
