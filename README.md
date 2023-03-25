# to run the app
On Linux
$ source .venv/bin/activate

On Windows
$ .venv\Scripts\activate

$ uvicorn main:app --reload --port 8000

# If you want the app to be accessible to all users on the local network, use the following command:

$ uvicorn main:app --realod --host 0.0.0.0 --port 8000