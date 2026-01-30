#!/usr/bin/env python
"""
Add password_hash column to users table
Run this once to fix the database schema
"""
import os
from sqlalchemy import create_engine, text

# Get database URL from environment
database_url = os.getenv('DATABASE_URL', 'postgresql://support_user:f3WWVsct38BGih3647K0ApygtjbS6dJs@dpg-d5s7rai4d50c73d5or50-a.oregon-postgres.render.com/support_dashboard')

# Fix postgres:// to postgresql://
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

print(f"Connecting to database...")
engine = create_engine(database_url)

try:
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='password_hash'
        """))

        if result.fetchone():
            print("✓ password_hash column already exists")
        else:
            print("Adding password_hash column to users table...")
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN password_hash VARCHAR(255)
            """))
            conn.commit()
            print("✓ password_hash column added successfully")

        # Check and add other missing columns
        columns_to_add = [
            ('last_login', 'TIMESTAMP'),
            ('is_active', 'BOOLEAN DEFAULT TRUE')
        ]

        for col_name, col_type in columns_to_add:
            result = conn.execute(text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='users' AND column_name='{col_name}'
            """))

            if result.fetchone():
                print(f"✓ {col_name} column already exists")
            else:
                print(f"Adding {col_name} column...")
                conn.execute(text(f"""
                    ALTER TABLE users
                    ADD COLUMN {col_name} {col_type}
                """))
                conn.commit()
                print(f"✓ {col_name} column added successfully")

        print("\n✅ Database migration completed successfully!")

except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
