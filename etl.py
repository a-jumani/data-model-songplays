import argparse
import glob
import os
import pandas as pd
import psycopg2
import textwrap
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Insert data present in file at filepath as record into songs and artists
    tables.

    Args:
        cur cursor to Postgres db
        filepath absolute path to a file in data/song_data
    Returns:
        None
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df.loc[0, ["song_id", "title", "artist_id", "year", "duration"]
                       ].apply(str).values.tolist()
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = df.loc[0, ["artist_id", "artist_name", "artist_location",
                             "artist_latitude", "artist_longitude"]
                         ].values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Insert data present in file at filepath as record into songplays, users
    and time tables.

    Args:
        cur cursor to Postgres db
        filepath absolute path to a file in data/log_data
    Returns:
        None
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    df["ts"] = pd.to_datetime(df["ts"], unit='ms')

    # insert all time data records found
    time_data = df["ts"].apply(lambda x: [x, x.hour, x.day, x.weekofyear,
                                          x.month, x.year, x.dayofweek]
                               ).tolist()
    column_labels = ("start_time", "hour", "day", "week", "month", "year",
                     "weekday")
    time_df = pd.DataFrame(time_data, columns=column_labels)
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.loc[:, ["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        # insert NULL if search was unsuccessful
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row[17], songid, artistid, row[15], row[7], row[12],
                         row[8], row[16])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Process all files in filepath using func.

    Args:
        cur cursor to Postgres db
        conn connection to Postgres db
        filepath "data/log_data" or "data/song_data"
        func process_log_file or process_song_file respectively
    Returns:
        None
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("\
            Load song play logs and song metadata to Postgres. The script \n\
            assumes that logs are stored under ./data/log_data and song \n\
            metadata under ./data/song_data")
    )

    # obtain postgres connection parameters
    for arg in ["host", "dbname", "user", "password"]:
        parser.add_argument("--" + arg, required=True)
    args = parser.parse_args()

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={}".format(
            args.host,
            args.dbname,
            args.user,
            args.password
        )
    )
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()
