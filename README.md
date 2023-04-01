# to run the app
$ pip install -r requirements.txt

# extract the downloaded files from from https://github.com/BtbN/FFmpeg-Builds/releases, add the route to the system path.

On Linux
$ source .venv/bin/activate

On Windows
$ .venv\Scripts\activate

$ uvicorn main:app --reload --port 8000

# If you want the app to be accessible to all users on the local network, use the following command:

$ uvicorn main:app --realod --host 0.0.0.0 --port 8000


# dockerize the app
$ docker build -t smart-languages-back:0.0.1 .
$ docker run -d -p 8000:8000 --name smart-languages-back-container smart-languages-back:0.0.1
