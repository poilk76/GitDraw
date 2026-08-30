from flask import Flask, request
from json import load,dump
from pathlib import Path
from threading import Thread

app = Flask(__name__)
PROGRAM_FOLDER_PATH = Path(__file__).parent
with open(PROGRAM_FOLDER_PATH/'settings.json','r') as f:
    settings = load(f)
QUE_PATH = PROGRAM_FOLDER_PATH/'que.json'
if not QUE_PATH.exists():
    with open(QUE_PATH,'r') as f: queue = load(f)
else:
    queue = []

@app.route("/add",methods=['POST'])
def add():
    global queue

    data = request.get_json()

    if data["priority"] == 0:

        queue.append(" ".join(data['command']))

    elif data["priority"] == 1:

        queue.insert(0," ".join(data['command']))

    with open(QUE_PATH,'w+') as f:
       dump(queue,f)

    return "DONE!", 200

@app.route("/",methods=['GET'])
def index():

    return "hi!"

def scheduler():

    pass

if __name__ == "__main__":

    server_thread = Thread(target=app.run,kwargs={"host":settings["QUE_SERVER"].split(":")[0],"port":settings["QUE_SERVER"].split(":")[1]})
    git_exec_scheduler = Thread(target=scheduler)

    