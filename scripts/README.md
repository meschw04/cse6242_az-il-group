### Dependencies

The codebase requires Python 3.x or higher to run

Install the dependencies using requirements.txt.

```sh
$ pip install -r requirements.txt
```
The UI is optimized for Google Chrome.
### Execution
Our application uses Flask to render the frontend. To start the application and use the interactive UI, execute application.py script

```sh
$ python application.py
```
Then open the UI on http://localhost:5000/

### Directory structure

Our code base comprises of the following important scripts and data files:

- application.py: this script is to render the Flask UI. It consists of methods to execute the required steps to accept inputs from UI and generate desired results.
- run_autoencoder.py: this runs the Autoencoder to generate album art.
- album_bokeh.py: the graphs based on user's selection of artist, album and nodes are created using this script. It also consists of functions to suggest users artist or album names in case they misspell a name or suggest in case we do not have the entered name in our dataset.
- lastfm_api_calls.py: This script was used to collect data for our project from LastFM API.
- dataset.csv: Our extracted dataset that contains album names, artist names, playcount, listneners, similar albums,image link,image path and tags.
- static: this folder consists of css and js dependency folders and other files that are required during execution. Images or graphs generated during the process of execution are saved in the img folder.
- templates: this folder consists of our HTML files.

All other scripts or files in our code base are utilized in one or more of the above mentioned scripts for execution.


