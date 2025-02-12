# Shamzam
A Shazam-like MVP for the ECM3408 Coursework Assignment

Uses a RESTful API built with Python and Flask to enable administrators to add, remove, and list music in an SQLite3 database.

## Installation

1. Clone the repository

2. Install the dependencies with conda

`conda create --name <env> --file requirements.txt`

3. If you have cloned from this repo you will need to create a .env file in the root of the directory and add the following inside

`AUDD_KEY="{YOUR_AUDD.IO_API_KEY}"

## Usage
Run the tracks.py script:

`python tracks.py`

By default the script will run on `http://localhost:3000`

You can use the following provided cURL commands to add, remove, list and identify tracks.

#### Insert a track
`curl -X POST http://localhost:3000/tracks \
-H "Content-Type: application/json" \
-d '{"trackname": "{trackname}", "filepath": "{filepath}"}'`

#### Delete a track
`curl -X DELETE http://localhost:3000/tracks \
-H "Content-Type: application/json" \
-d '{"trackname": "{trackname}"}`

#### Get all tracks
`curl -X GET http://localhost:3000/tracks \
-H "Accept: application/json"` 

#### Identify track
`curl -X POST http://127.0.0.1:3000/identify \
-H "Content-Type: application/json" \
-d '{"file_path": "{filepath}"}'`


## User Stories

- S1: As an administrator, I want to add a music track to the catalogue, so that a user
    can listen to it.
- S2: As an administrator, I want to remove a music track from the catalogue, so that a
    user cannot listen to it.
- S3: As an administrator, I want to list the names of the music tracks in the catalogue,
    so that I know what it contains.
- S4: As a user, I want to convert a music fragment to a music track in the catalogue, so
    that I can listen to it.
  