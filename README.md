# Data Model and ETL for Song Play Logs using Amazon RDS for PostgreSQL

## Objectives
Aims of the project are as follows:
1. Create a data model to store and analyze user song play logs together with songs metadata.
2. Write an ETL to load raw data from JSON files into a PostgreSQL instance.
3. Test the loaded data.

## Schema
The database uses the STAR schema to model the user logs. The fact table contains songs users played. The dimension tables contain additional properties of users, songs, artists and the times at which the songs were played. The benefits of this schema are as follows:
- Data exploration is easy since even complex queries on STAR schema require only a small set of simple JOIN's.
- The tables are sufficiently denormalized to ensure the queries execute fast.

*Note: this schema is not ideal for a write-heavy workload. But is quite performant for analytics.*

## Files
Project has the following main files:
- `create_tables.py` resets all tables in the database. Execute `python create_tables.py -h` to see usage.
- `etl.py` populates the database using data residing in JSON files locally. Execute `python etl.py -h` to see usage.
- `sql_queries.py` contains queries used to create tables, insert data into tables and search some data

*Note: the scripts were tested on Python 3.*

## Example Queries on Dummy Data
1. Females listen to 88.5% more songs than males on average. Relevant queries:
- Number of users by gender: `SELECT gender, COUNT(*) FROM users GROUP BY gender`
- Song plays by gender: `SELECT users.gender, COUNT(*) FROM (songplays JOIN users ON songplays.user_id=users.user_id) GROUP BY users.gender`
2. Paid users listen to 15.3 times more songs than free users on average. Relevant queries:
- Number of users by paid/free: `SELECT level, COUNT(*) FROM users GROUP BY level`
- Number of plays by paid/free: `SELECT level, COUNT(*) FROM songplays GROUP BY level`
3. On average, most requests are received on Wednesday followed by Friday, and the least over the weekend. Relevant query:
- Number of plays by day of the week: `SELECT time.weekday, COUNT(*) FROM songplays JOIN time ON songplays.start_time=time.start_time GROUP BY time.weekday ORDER BY time.weekday`
