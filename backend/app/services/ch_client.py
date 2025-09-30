import os
from typing import Any

import clickhouse_connect


def get_client():
    url = os.getenv('CLICKHOUSE_URL', 'http://clickhouse:8123')
    # Parse simple http url
    host_port = url.replace('http://','').replace('https://','')
    host, port = host_port.split(':')
    return clickhouse_connect.get_client(host=host, port=int(port))


def write_dataframe(df, table: str) -> None:
    client = get_client()
    client.command(f'CREATE TABLE IF NOT EXISTS {table} AS SELECT * FROM system.one WHERE 1=0')
    client.insert_df(table, df)


