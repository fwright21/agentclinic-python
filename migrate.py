#!/usr/bin/env python3
"""
Run all SQL migrations in the migrations/ directory.
Creates the database if it doesn't exist.
"""

import asyncio
import aiosqlite
import os
from pathlib import Path


MIGRATIONS_DIR = Path(__file__).parent / "migrations"
DB_PATH = Path(__file__).parent / "agentclinic.db"


async def run_migrations():
    # Get all .sql files sorted by name
    sql_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    if not sql_files:
        print("No migration files found.")
        return

    print(f"Found {len(sql_files)} migration(s)")

    async with aiosqlite.connect(DB_PATH) as db:
        for sql_file in sql_files:
            print(f"Running: {sql_file.name}")
            with open(sql_file, "r") as f:
                sql = f.read()
            await db.executescript(sql)
            await db.commit()

    print(f"Database ready: {DB_PATH}")


if __name__ == "__main__":
    asyncio.run(run_migrations())
