#!/usr/bin/env python3
import os
import tempfile

from heroserver.jobmanager.db import DB
from models import Action, Actor, Agent, Executor


def test_sqlite():
    """Test SQLite database connection and models."""
    print("\nTesting SQLite connection...")

    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name

    try:
        # Initialize SQLite database
        db = DB(db_type="sqlite", db_path=db_path)
        print("SQLite database initialized successfully")

        # Test model creation
        with db.db.atomic():
            # Create test executor
            executor = Executor.create(name="test_executor", description="Test executor")

            # Create test actor
            actor = Actor.create(name="test_actor", executor=executor, description="Test actor")

            # Create test action
            action = Action.create(name="test_action", actor=actor, description="Test action")

            # Create test agent
            agent = Agent.create(name="test_agent", description="Test agent")

            print("Test records created successfully")

            # Verify records
            assert Executor.get(Executor.name == "test_executor")
            assert Actor.get(Actor.name == "test_actor")
            assert Action.get(Action.name == "test_action")
            assert Agent.get(Agent.name == "test_agent")
            print("Record verification successful")

    except Exception as e:
        print(f"SQLite test failed: {str(e)}")
        raise
    finally:
        # Close connection
        if hasattr(db, "db"):
            db.db.close()
            print("SQLite connection closed successfully")

        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)


def test_postgresql():
    """Test PostgreSQL database connection and models."""
    print("\nTesting PostgreSQL connection...")

    try:
        # Initialize PostgreSQL database
        db = DB(db_type="postgresql", host="localhost", port=5432, dbname="postgres", user="postgres", password="admin")
        print("PostgreSQL database initialized successfully")

        # Test model creation
        with db.db.atomic():
            # Create test executor
            executor = Executor.create(name="test_executor_pg", description="Test executor PostgreSQL")

            # Create test actor
            actor = Actor.create(name="test_actor_pg", executor=executor, description="Test actor PostgreSQL")

            # Create test action
            action = Action.create(name="test_action_pg", actor=actor, description="Test action PostgreSQL")

            # Create test agent
            agent = Agent.create(name="test_agent_pg", description="Test agent PostgreSQL")

            print("Test records created successfully")

            # Verify records
            assert Executor.get(Executor.name == "test_executor_pg")
            assert Actor.get(Actor.name == "test_actor_pg")
            assert Action.get(Action.name == "test_action_pg")
            assert Agent.get(Agent.name == "test_agent_pg")
            print("Record verification successful")

            # Cleanup test data
            executor.delete_instance(recursive=True)
            agent.delete_instance(recursive=True)
            print("Test data cleaned up successfully")

    except Exception as e:
        print(f"PostgreSQL test failed: {str(e)}")
        raise
    finally:
        # Close connection
        if hasattr(db, "db"):
            db.db.close()
            print("PostgreSQL connection closed successfully")


def main():
    """Run all database tests."""
    print("Starting database tests...")

    try:
        # Test SQLite
        test_sqlite()
        print("SQLite test completed successfully")

        # Test PostgreSQL
        test_postgresql()
        print("PostgreSQL test completed successfully")

        print("\nAll tests completed successfully!")

    except Exception as e:
        print(f"\nTests failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
