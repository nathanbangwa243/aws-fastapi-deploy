# -*- coding: utf-8 -*-
import os
import pytest
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Load environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

@pytest.fixture(scope="module")
def mongo_client():
    """Initialize a MongoDB connection for testing."""
    client = MongoClient(MONGO_URI)
    yield client
    client.close()

@pytest.fixture(scope="module")
def test_db(mongo_client):
    """Retrieve a reference to the test database."""
    db = mongo_client[MONGO_DB_NAME]
    yield db

def test_mongo_connection(mongo_client):
    """Verify that the MongoDB connection is established."""
    try:
        mongo_client.admin.command("ping")
    except ConnectionFailure:
        pytest.fail("Failed to connect to MongoDB")

def test_database_exists(test_db):
    """Check if the specified database is accessible."""
    db_list = test_db.client.list_database_names()
    assert MONGO_DB_NAME in db_list, f"Database {MONGO_DB_NAME} does not exist"

def test_collections_exist(test_db):
    """Ensure that the database contains at least one collection."""
    collections = test_db.list_collection_names()
    assert len(collections) > 0, "No collections found in the database"
