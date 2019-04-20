Dependencies
The codebase requires Python 3.6 or higher to run. It requires the following libraries to be installed:

bokeh=1.0.4
Flask=1.0.2
flask_cors=3.0.7
Keras=2.2.4
matplotlib=3.0.3
networkx=2.2
numpy=1.16.2
opencv-python=4.1.0.25
pandas=0.24.2
tensorflow=1.13.1
editdistance=0.5.3

Install the dependencies using requirements.txt.

$ pip install -r requirements.txt


Execution
Our application uses Flask to render the frontend. To start the application and use the interactive UI, execute application.py script

$ python application.py
Then open the UI on http://localhost:5000/
The UI is optimized for Google Chrome.


Description
Our code base comprises of the following important scripts and data files:

	application.py: this script is to render the Flask UI. It consists of methods to execute the required steps to accept inputs from UI and generate desired results.
	run_autoencoder.py: this runs the Autoencoder to generate album art.
	album_bokeh.py: the graphs based on user’s selection of artist, album and nodes are created using this script. It also consists of functions to suggest users artist or album names in case they misspell a name or to suggest in case we do not have the entered name in our dataset. 
	lastfm_api_calls.py: This script was used to collect and preprocess data for our project from LastFM API.
	dataset.csv: Our extracted dataset that contains album names, artist names, playcount, listneners, similar albums,image link,image path and tags.
	static: this folder consists of css and js dependency folders and other files that are required during execution. Images or graphs generated during the process of execution are saved in the img folder.
	templates: this folder consists of our HTML files for UI.

All other scripts or files in our code base are utilized in one or more of the above mentioned scripts for execution.

To pull data from LastFM API, follow the instructions in the below link to register for an API key:
	https://www.last.fm/api/account/create

For now, the authors have provided an API key in code(lastfm_api_calls.py) but it can be replaced with a new key after registration.

The run_autoencoder.py script loads the existing models to generate album covers that the users see on UI. But to build a new model or change the existing model, 2-autoencoder.ipynb must be used.

