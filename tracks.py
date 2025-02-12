import database
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)


@app.route("/tracks", methods=["POST"])
def add_track():
    """Add a track to the database."""

    js = request.get_json()
    trackname = js.get("trackname")
    filepath = js.get("filepath")

    if not os.path.isfile(filepath):
        return jsonify({"message": "Bad Request. File does not exist at the given filepath."}), 400

    if not trackname:
        return jsonify({"message": "Bad Request. 'trackname' is required."}), 400

    if not filepath:
        return jsonify({"message": "Bad Request. 'filepath' is required."}), 400

    existing_track = database.db.lookup(trackname)
    if existing_track is not None:
        return jsonify({"message": "Track already present in database."}), 409

    if database.db.insert(js):
        return jsonify({"message": "Track added successfully!"}), 201
    else:
        return jsonify({"message": "Track insertion failed."}), 500


@app.route("/tracks", methods=["DELETE"])
def delete_track():
    """Deletes a track from the database."""

    try:
        trackname = request.json.get('trackname')
    except:
        return jsonify({"message": "Invalid JSON format."}), 400

    if trackname:
        try:
            if database.db.lookup(trackname) is not None:
                deleted_count = database.db.delete_track(trackname)
                if deleted_count == 1:
                    return jsonify({"message": "Track successfully deleted."}), 200
                elif deleted_count > 1:
                    return jsonify({"message": "Multiple tracks deleted"}), 200
                else:
                    return jsonify({"message": "Track deletion failed."}), 500
            else:
                return jsonify({"message": "Track not found."}), 404
        except:
            return jsonify({"message": "Failed to delete the track."}), 500
    else:
        return jsonify({"message": "'trackname' is required."}), 400


@app.route("/tracks", methods=["GET"])
def get_tracks():
    """Returns a list of all the tracks currently in the database."""

    if "Accept" not in request.headers or request.headers["Accept"] != "application/json":
        return jsonify({"message": "Bad Request: Accept header must be 'application/json'."}), 400

    try:
        tracknames = database.db.list_tracks()
        if tracknames:
            return jsonify({"tracknames": tracknames}), 200
        else:
            return jsonify({"message": "No tracks found."}), 404

    except Exception as e:
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500


@app.route('/identify', methods=['POST'])
def identify_song():
    """Takes a filepath to a music file from which the AudD.io API will
       attempt to recognise the song. If the database contains this
       song the relevant row will be returned."""

    api_token = os.getenv("AUDD_KEY")
    if not api_token:
        return {"error": "Missing API key"}, 401

    file_path = request.json.get("file_path")
    if not file_path:
        return jsonify({"error": "file_path is required"}), 400

    if not os.path.isfile(file_path):
        return jsonify({"error": "File does not exist or is inaccessible"}), 400

    files = {'file': open(file_path, 'rb')}
    data = {'api_token': api_token, 'return': 'title'}

    response = requests.post('https://api.audd.io/', files=files, data=data)
    result = response.json()

    if result.get("status") == "success" and result.get("result"):
        row = database.db.lookup(result["result"]["title"])
        if row:
            return jsonify(row), 200
        else:
            return jsonify({"error": "Song not found in database."}), 404
    else:
        return jsonify({"error": "Song not recognised by AudD.io."}), 404


if __name__ == "__main__":
    app.run(host="localhost", port=3000, debug=True)
