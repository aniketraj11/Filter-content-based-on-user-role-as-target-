from flask import Flask, jsonify, request
from difflib import SequenceMatcher
from operator import itemgetter
import pprint
import json

app = Flask(__name__)
users = [
    ["manager" , "a,c"],
    ["director","a,b,c,d"],
    ["intern" , "a"]
]
contentTag = [
    {
        "id": "content 1",
        "tag": "a,c"
      },
    {
        "id": "content 2",
        "tag": "a"
    },
{
        "id": "content 3",
        "tag": "a,c,d"
      }
]
output = []

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def myfunc():
    output = []
    for user in users:
        for content in contentTag:
            output.append([user[0], user[1], content['id'], content['tag'], similar(user[1], content['tag'])])


    sortedOutput = sorted(output, key=itemgetter(0, 4), reverse=True)
    return sortedOutput

def withParam(role):
    output = []
    search = role
    user = []
    flag = False
    for user in users:
        if user[0] == search:
            print("Found it!", user)
            flag = True
            break

    if flag == False :
        return ['Role not found']

    for content in contentTag:
        output.append([user[0], user[1], content['id'], content['tag'], similar(user[1], content['tag'])])

    sortedOutput = sorted(output, key=itemgetter(0, 4), reverse=True)

    return sortedOutput


@app.route("/")
def home():
    d = myfunc()
    return jsonify(d)

@app.route("/user")
def forRole():
    my_var = request.args.get('role', None)
    d = withParam(my_var)
    return jsonify(d)

if __name__ == "__main__":
    app.run(debug=True)


