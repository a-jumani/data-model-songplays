import argparse
import psycopg2
import textwrap
from sql_queries import *

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("\
            Initialize the database.")
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

    # drop all tables
    for query in drop_table_queries:
        cur.execute(query)

    # create all tables
    for query in create_table_queries:
        cur.execute(query)
