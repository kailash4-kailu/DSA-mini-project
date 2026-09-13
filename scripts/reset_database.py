"""
Database Reset Script
Drops and recreates the iot_streaming database tables.
"""
import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mysql.connector
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def reset_database():
    """Drop and recreate database tables."""
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "changeme_secret"),
    )
    cursor = conn.cursor()

    db_name = os.getenv("MYSQL_DATABASE", "iot_streaming")

    logger.info("Dropping and recreating database '%s'…", db_name)
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cursor.execute(f"CREATE DATABASE {db_name}")
    cursor.execute(f"USE {db_name}")

    # Read schema file
    schema_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "database", "schema.sql"
    )
    with open(schema_path, "r") as f:
        schema = f.read()

    # Execute each statement
    for statement in schema.split(";"):
        stmt = statement.strip()
        if stmt and not stmt.startswith("--"):
            try:
                cursor.execute(stmt)
            except mysql.connector.Error as e:
                # Skip harmless errors like CREATE DATABASE IF NOT EXISTS
                if e.errno not in (1007, 1049):
                    logger.warning("SQL warning: %s", e)

    conn.commit()
    cursor.close()
    conn.close()
    logger.info("Database '%s' reset successfully.", db_name)


if __name__ == "__main__":
    reset_database()
