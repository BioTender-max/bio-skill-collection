#!/usr/bin/env python3
"""
Example: Explore a database in JGI Lakehouse
Shows how to list schemas, tables, and sample data
"""

import os
import sys

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from rest_client import (
    execute_sql,
    query,
    list_catalogs,
    show_schemas
)


def explore_database(database_name: str = "GOLD"):
    """Explore a database and show its contents"""

    print(f"{'='*80}")
    print(f"Exploring {database_name} Database")
    print(f"{'='*80}\n")

    # 1. List all schemas
    print("1. Available Schemas:")
    print("-" * 80)
    try:
        schemas = show_schemas()
        for schema in schemas:
            marker = "✓" if schema == database_name else " "
            print(f"  {marker} {schema}")
        print()

        if database_name not in schemas:
            print(f"⚠️  {database_name} not found in available schemas")
            return

    except Exception as e:
        print(f"❌ Error listing schemas: {e}\n")
        return

    # 2. List tables in database
    print(f"2. Tables in {database_name}:")
    print("-" * 80)
    try:
        tables = query(f"SHOW TABLES IN {database_name}")
        table_names = [t.get("TABLE_NAME") for t in tables]
        print(f"  Found {len(table_names)} tables:")
        for table in table_names:
            print(f"    - {table}")
        print()
    except Exception as e:
        print(f"❌ Error listing tables: {e}\n")
        return

    # 3. Explore first few tables
    print(f"3. Table Details (first 3 tables):")
    print("-" * 80)
    for table in table_names[:3]:
        print(f"\nTable: {database_name}.{table}")
        print("  " + "-" * 76)

        # Get schema
        try:
            schema = query(f"DESCRIBE {database_name}.{table}")
            print(f"  Columns ({len(schema)}):")
            for col in schema[:10]:
                name = col.get("COLUMN_NAME")
                dtype = col.get("DATA_TYPE")
                print(f"    - {name}: {dtype}")
            if len(schema) > 10:
                print(f"    ... and {len(schema) - 10} more columns")
        except Exception as e:
            print(f"  ❌ Error getting schema: {e}")

        # Get row count
        try:
            count_result = query(f"SELECT COUNT(*) as cnt FROM {database_name}.{table}")
            count = count_result[0].get("cnt") if count_result else "?"
            print(f"  Row count: {count:,}" if isinstance(count, int) else f"  Row count: {count}")
        except:
            print("  Row count: (unable to determine)")

        # Get sample
        try:
            sample = query(f"SELECT * FROM {database_name}.{table} LIMIT 2")
            if sample:
                print(f"  Sample data:")
                for i, row in enumerate(sample, 1):
                    print(f"    Row {i}: {len(row)} fields")
                    # Show first 3 fields
                    for k, v in list(row.items())[:3]:
                        val = str(v)[:50]
                        print(f"      {k}: {val}")
        except:
            print("  Sample: (unable to retrieve)")

    print(f"\n{'='*80}")
    print(f"✅ Exploration complete!")
    print(f"{'='*80}")
    print(f"\nAll {database_name} tables:")
    for table in table_names:
        print(f"  - {database_name}.{table}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Explore JGI Lakehouse databases")
    parser.add_argument("database", nargs="?", default="GOLD",
                       help="Database name to explore (default: GOLD)")
    args = parser.parse_args()

    # Check token
    if not os.getenv("DREMIO_PAT"):
        print("❌ DREMIO_PAT not set")
        print("Run: export DREMIO_PAT=$(cat ~/.secrets/dremio_pat)")
        sys.exit(1)

    explore_database(args.database)
