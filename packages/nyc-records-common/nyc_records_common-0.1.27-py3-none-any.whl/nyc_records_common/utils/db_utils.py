# src/nyc_records_common/utils/db_utils.py
"""Database utility functions."""


def convert_connection_string(original: str) -> str:
    """
    Converts a SQL Server style connection string to psycopg2 compatible DSN.

    Args:
        original (str): Original connection string (e.g., from Google Secret Manager).

    Returns:
        str: psycopg2-compatible connection string.
    """
    parts = original.split(";")
    dsn_parts = []
    mapping = {
        "Server": "host",
        "Port": "port",
        "Database": "dbname",
        "User ID": "user",
        "Password": "password",
    }
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            if key in mapping:
                dsn_parts.append(f"{mapping[key]}={value}")
    return " ".join(dsn_parts)


def convert_to_postgres_dsn(original: str) -> str:
    """
    Convert a SQL Server style connection string to psycopg2 compatible DSN.

    Args:
        original (str): Original connection string (e.g., from Google Secret Manager).

    Returns:
        str: psycopg2-compatible connection string.
    """
    parts = original.split(";")
    connection_data = {}

    mapping = {
        "Server": "host",
        "Port": "port",
        "Database": "dbname",
        "User ID": "user",
        "Password": "password",
    }

    # Parse out the parts
    for part in parts:
        if "=" in part:
            key, value = part.split("=", 1)
            key, value = key.strip(), value.strip()
            if key in mapping:
                connection_data[mapping[key]] = value

    # Build the DSN
    # e.g. postgresql://user:password@host:port/dbname
    user = connection_data.get("user", "")
    password = connection_data.get("password", "")
    host = connection_data.get("host", "")
    port = connection_data.get("port", "")
    dbname = connection_data.get("dbname", "")

    # Construct the DSN
    dsn = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    return dsn