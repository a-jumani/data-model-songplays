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
