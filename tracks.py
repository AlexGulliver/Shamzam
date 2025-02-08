import database

from flask import Flask, request

app = Flask(__name__)

@app.route("/tracks/<string:code>",methods=["PUT"])
def endpoint1(code):
    js = request.get_json()
    code2 = js["code"]
    name = js["name"]
    if code2 != None and name != None and code == code2:
        track = {"code": code, "name": name}
        if database.db.lookup(code) != None:
            if database.db.update(js):
                return " ", 204 # No Content
            else:
                return " ", 500 # Internal Server Error
        else:
            if database.db.insert(js):
                return " ", 201 # Created
            else:
                return " ", 500 # Internal Server Error
    else:
        return " ", 400 # Bad Request
    
if __name__ == "__main__":
    app.run(host="localhost", port=3000)