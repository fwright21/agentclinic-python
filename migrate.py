#!/usr/bin/env python3
"""
Run all SQL migrations in the migrations/ directory.
Tracks applied migrations in a _migrations table to avoid re-running.
"""

import asyncio
import aiosqlite
from pathlib import Path


MIGRATIONS_DIR = Path(__file__).parent / "migrations"
DB_PATH = Path(__file__).parent / "agentclinic.db"


async def run_migrations():
    sql_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

    if not sql_files:
        print("No migration files found.")
        return

    print(f"Found {len(sql_files)} migration(s)")

    async with aiosqlite.connect(DB_PATH) as db:
        # Create migrations tracking table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                filename TEXT PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

        for sql_file in sql_files:
            # Check if already applied
            async with db.execute(
                "SELECT filename FROM _migrations WHERE filename = ?", (sql_file.name,)
            ) as cursor:
                already_applied = await cursor.fetchone()

            if already_applied:
                print(f"Skipping (already applied): {sql_file.name}")
                continue

            print(f"Running: {sql_file.name}")
            with open(sql_file, "r") as f:
                sql = f.read()
            await db.executescript(sql)
            await db.execute(
                "INSERT INTO _migrations (filename) VALUES (?)", (sql_file.name,)
            )
            await db.commit()

    print(f"Database ready: {DB_PATH}")


if __name__ == "__main__":
    asyncio.run(run_migrations())
