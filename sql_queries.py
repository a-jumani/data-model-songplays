# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id BIGSERIAL PRIMARY KEY,
        user_id     INTEGER NOT NULL,
        song_id     CHAR(18),
        artist_id   CHAR(18),
        start_time  TIMESTAMP(3) NOT NULL,
        level       CHAR(4) NOT NULL,
        session_id  BIGINT NOT NULL,
        location    TEXT,
        user_agent  TEXT
    )
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id    INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name  TEXT NOT NULL,
        gender     CHAR,
        level      CHAR(4) NOT NULL
    )
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id   CHAR(18) PRIMARY KEY,
        title     TEXT NOT NULL,
        artist_id CHAR(18) NOT NULL,
        year      INTEGER NOT NULL,
        duration  NUMERIC(10, 6) NOT NULL
    )
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id CHAR(18) PRIMARY KEY,
        name      TEXT NOT NULL,
        location  TEXT,
        latitude  NUMERIC(8, 5),
        longitude NUMERIC(8, 5)
    )
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP(3) PRIMARY KEY,
        hour       SMALLINT NOT NULL,
        day        SMALLINT NOT NULL,
        week       SMALLINT NOT NULL,
        month      SMALLINT NOT NULL,
        year       SMALLINT NOT NULL,
        weekday    SMALLINT NOT NULL
    )
""")

# INSERT RECORDS

# assumption: all plays are unique
songplay_table_insert = ("""
    INSERT INTO songplays (user_id, song_id, artist_id, start_time, level,
        session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

# on conflict, latest level will be stored against the user
# assumption: log_data will be inserted chronologically (otherwise start_time
# will need to be part of the table)
user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO UPDATE
        SET level=EXCLUDED.level
""")

# assumption: not expecting missing fields
song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id)
    DO NOTHING
""")

# on conflict, update (location, latitude, longitude) fields if need be
# assumption: in-existence of duplicate, non-blank (location, latitude,
# longitude) fields
artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO UPDATE
        SET location=EXCLUDED.location, latitude=EXCLUDED.latitude,
            longitude=EXCLUDED.longitude
        WHERE artists.location = ''
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time)
    DO NOTHING
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create,
                        song_table_create, artist_table_create,
                        time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop,
                      artist_table_drop, time_table_drop]
