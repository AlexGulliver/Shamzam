import unittest
import requests
import sqlite3

tracks = "http://localhost:3000/tracks"
identify = "http://localhost:3000/identify"


class Testing(unittest.TestCase):

    def test_US1H(self):
        # User Story 1 Happy Path: successful track insertion

        # Clear database before starting tests
        conn = sqlite3.connect('tracks.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tracks")
        conn.commit()
        conn.close()

        trackname = "Blinding Lights"
        filepath = "./songs/Blinding Lights.wav"

        payload = {"trackname": trackname, "filepath": filepath}
        response = requests.post(tracks, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 201:
            json_response = response.json()
            self.assertEqual(json_response["message"], "Track added successfully!")
        else:
            self.assertIn(
                response.status_code, [201, 400, 409, 500], f"Unexpected status code: {response.status_code}"
                )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US1U1(self):
        # User Story 1 Unhappy Path 1: invalid file path
        trackname = "Blinding Lights"
        filepath = "./songs/InvalidSong.wav"

        payload = {"trackname": trackname, "filepath": filepath}
        response = requests.post(tracks, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 400:
            json_response = response.json()
            self.assertEqual(
                json_response["message"], "Bad Request. File does not exist at the given filepath."
                )
        else:
            self.assertIn(
                response.status_code, [201, 400, 409, 500], f"Unexpected status code: {response.status_code}"
                )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US1U2(self):
        # User Story 1 Unhappy Path 2: trackname not included
        trackname = ""
        filepath = "./songs/Blinding Lights.wav"

        payload = {"trackname": trackname, "filepath": filepath}
        response = requests.post(tracks, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 400:
            json_response = response.json()
            self.assertEqual(
                json_response["message"], "Bad Request. 'trackname' is required."
                )
        else:
            self.assertIn(
                response.status_code, [201, 400, 409, 500], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US1U3(self):
        # User Story 1 Unhappy Path 3: track already exists in the database
        trackname = "Blinding Lights"
        filepath = "./songs/Blinding Lights.wav"

        payload = {"trackname": trackname, "filepath": filepath}
        response = requests.post(tracks, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 409:
            json_response = response.json()
            self.assertEqual(
                json_response["message"], "Track already present in database."
                )
        else:
            self.assertIn(
                response.status_code, [201, 400, 409, 500], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US2H(self):
        # User Story 2 Happy Path: successful track deletion
        trackname = "Blinding Lights"

        payload = {"trackname": trackname}
        response = requests.delete(tracks, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 200:
            json_response = response.json()
            self.assertEqual(json_response["message"], "Track successfully deleted.")
        else:
            self.assertIn(
                response.status_code, [200, 400, 404, 500], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US2U1(self):
        # User Story 2 Unhappy Path 1: track not found
        trackname = "Blinding Fights"

        payload = {"trackname": trackname}
        response = requests.delete(tracks, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 404:
            json_response = response.json()
            self.assertEqual(json_response["message"], "Track not found.")
        else:
            self.assertIn(
                response.status_code, [200, 400, 404, 500], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US2U2(self):
        # User Story 2 Unhappy Path 2: no trackname provided
        trackname = ""

        payload = {"trackname": trackname}
        response = requests.delete(tracks, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 400:
            json_response = response.json()
            self.assertEqual(json_response["message"], "'trackname' is required.")
        else:
            self.assertIn(
                response.status_code, [200, 400, 404, 500], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US2U3(self):
        # User Story 2 Unhappy Path 3: invalid json input
        payload = "{trackname: Blinding Lights}"

        response = requests.delete(tracks, data=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 400:
            json_response = response.json()
            self.assertEqual(json_response["message"], "Invalid JSON format.")
        else:
            self.assertIn(
                response.status_code, [200, 400, 404, 500], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US3H(self):
        # User Story 3 Happy Path: add a track and then list track names
        trackname = "Blinding Lights"
        filepath = "./songs/Blinding Lights.wav"

        # Add the track
        payload = {"trackname": trackname, "filepath": filepath}
        post_response = requests.post(tracks, json=payload, headers={"Content-Type": "application/json"})

        self.assertEqual(post_response.status_code, 201, f"Failed to add track: {post_response.text}")

        response = requests.get(tracks, headers={"Accept": "application/json"})

        if response.status_code == 200:
            json_response = response.json()
            self.assertIsNotNone(json_response)
            self.assertIn(
                trackname, json_response.get("tracknames", []), f"Track '{trackname}' was not found in the list."
            )
        else:
            self.assertIn(
                response.status_code, [200, 400, 404, 500], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US3U1(self):
        # User Story 3 Unhappy Path 1: no tracks in database
        trackname = "Blinding Lights"

        payload = {"trackname": trackname}
        delete_response = requests.delete(tracks, json=payload, headers={"Content-Type": "application/json"})
        self.assertEqual(delete_response.status_code, 200, f"Failed to delete track: {delete_response.text}")

        response = requests.get(tracks, headers={"Accept": "application/json"})

        if response.status_code == 404:
            json_response = response.json()
            self.assertEqual(json_response["message"], "No tracks found.")
        else:
            self.assertIn(
                response.status_code, [200, 400, 404, 500], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US3U2(self):
        # User Story 3 Unhappy Path 2: Missing Accept header
        response = requests.get(tracks)

        self.assertEqual(response.status_code, 400, f"Unexpected status code: {response.status_code}")
        json_response = response.json()
        self.assertEqual(json_response["message"], "Bad Request: Accept header must be 'application/json'.")

    def test_US3U3(self):
        # User Story 3 Unhappy Path 3: Invalid Accept header
        response = requests.get(tracks, headers={"Accept": "text/plain"})  # Invalid Accept header

        self.assertEqual(response.status_code, 400, f"Unexpected status code: {response.status_code}")
        json_response = response.json()
        self.assertEqual(json_response["message"], "Bad Request: Accept header must be 'application/json'.")

    def test_US4H(self):
        # User Story 4 Happy Path: identify a track in the database and return the row
        trackname = "Blinding Lights"
        filepath = "./songs/Blinding Lights.wav"

        # Add the track
        payload = {"trackname": trackname, "filepath": filepath}
        requests.post(tracks, json=payload, headers={"Content-Type": "application/json"})

        fragment_filepath = "./songs/~Blinding Lights.wav"

        payload = {"filepath": fragment_filepath}
        response = requests.post(identify, json=payload, headers={"Content-Type": "application/json"})
        if response.status_code == 200:
            # Expected response
            expected_response = {
                "filepath": "./songs/Blinding Lights.wav",
                "trackname": "Blinding Lights"
            }

            # Assert that the response JSON matches the expected response
            self.assertEqual(
                response.json(), expected_response, "Response JSON does not match the expected output."
            )
        else:
            self.assertIn(
                response.status_code, [200, 400, 401, 404], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US4U1(self):
        # User Story 4 Unhappy Path 1: song is not recognised by AudD.io
        filepath = "./songs/~Davos.wav"

        payload = {"filepath": filepath}
        response = requests.post(identify, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 404:
            json_response = response.json()
            self.assertEqual(
                json_response["error"], "Song not recognised by AudD.io."
            )
        else:
            self.assertIn(
                response.status_code, [200, 400, 401, 404], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US4U2(self):
        # User Story 4 Unhappy Path 2: invalid file path
        filepath = "invalid_file_path"

        payload = {"filepath": filepath}
        response = requests.post(identify, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 400:
            json_response = response.json()
            self.assertEqual(
                json_response["error"], "File does not exist or is inaccessible"
            )
        else:
            self.assertIn(
                response.status_code, [200, 400, 401, 404], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")

    def test_US4U3(self):
        # User Story 4 Unhappy Path: no file path provided
        filepath = ""

        payload = {"filepath": filepath}
        response = requests.post(identify, json=payload, headers={"Content-Type": "application/json"})

        if response.status_code == 400:
            json_response = response.json()
            self.assertEqual(json_response["error"], "filepath is required")
        else:
            self.assertIn(
                response.status_code, [200, 400, 401, 404], f"Unexpected status code: {response.status_code}"
            )
            self.fail(f"Unexpected status code: {response.status_code} with message {response.text}")


if __name__ == "__main__":
    unittest.main()
