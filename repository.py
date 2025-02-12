import sqlite3
import os


class Repository:
    def __init__(self, table):
        self.table = table
        self.database = self.table + ".db"
        self.make()

    def make(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor . execute(
                f" CREATE TABLE IF NOT EXISTS {self.table} " +
                " (trackname TEXT PRIMARY KEY , filepath TEXT, filedata BLOB) "
            )
            connection.commit()

    def clear(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM {self.table}"
            )
            connection.commit()

    def insert(self, js):
        trackname = js.get("trackname")
        filepath = js.get("filepath")

        if trackname and filepath:
            if os.path.isfile(filepath):
                try:
                    with open(filepath, 'rb') as file:
                        bitstream = file.read()

                    with sqlite3.connect(self.database) as connection:
                        cursor = connection.cursor()
                        cursor.execute(
                            f"INSERT INTO {self.table} (trackname, filepath, filedata) VALUES (?, ?, ?)",
                            (trackname, filepath, bitstream)
                        )
                        connection.commit()

                    return cursor.rowcount

                except Exception as e:
                    print(f"Error inserting track: {e}")
                    return 0

            else:
                print("File not found at the given path.")
                return 0

        else:
            print("Trackname or filepath missing.")
            return 0

    def delete_track(self, trackname):
        """Deletes a track from the database based on the trackname."""
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM {self.table} WHERE trackname = ?", (trackname,)
            )
            connection.commit()
            return cursor.rowcount

    def lookup(self, trackname):
        try:
            with sqlite3.connect(self.database) as connection:
                cursor = connection.cursor()

                query = f"SELECT trackname, filepath FROM {self.table} WHERE trackname = ?"
                # print(f"Executing query: {query} with trackname = {trackname}")
                cursor.execute(query, (trackname,))
                row = cursor.fetchone()
                # print("Row fetched:", row)
                if row:
                    return {"trackname": row[0], "filepath": row[1]}
                else:
                    return None
        except Exception as e:
            print(f"Error during lookup: {e}")
            return None

    def list_tracks(self):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT trackname FROM {self.table}")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
