"""
Database initialization utility.
Run with: uv run python app/init_db.py [--seed]
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db, seed_db


def main():
    """Initialize database and optionally seed with data."""
    parser = argparse.ArgumentParser(description="Initialize Snake Showdown database")
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed database with mock players and scores"
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop existing tables before creating (WARNING: destroys data)"
    )
    
    args = parser.parse_args()
    
    # Drop tables if requested
    if args.drop:
        from app.database import drop_db
        print("⚠️  Dropping all tables...")
        drop_db()
        print("✅ Tables dropped")
    
    # Create tables
    print("📦 Creating database tables...")
    init_db()
    print("✅ Database initialized")
    
    # Seed data if requested
    if args.seed:
        print("🌱 Seeding database...")
        seed_db()
    
    print("🎉 Done!")


if __name__ == "__main__":
    main()
