
# -*- coding: utf-8 -*-

import os
import unittest
from fastapi.testclient import TestClient
from app.main import app
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from pydantic import BaseModel, Field


class Category(BaseModel):
    id: int = Field(..., alias="_id", description="Category ID")
    name: str
    description: str


class CategoryCreate(BaseModel):
    name: str
    description: str


class CategoryUpdate(BaseModel):
    name: str
    description: str


def get_db():
    try:
        client = MongoClient(os.environ["MONGO_URI_TEST"])
        db = client[os.environ["MONGO_DB_NAME_TEST"]]
        return db
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


class TestCategories(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.db = get_db()
        self.db.categories.delete_many({})

    def tearDown(self):
        self.db.categories.delete_many({})

    def test_get_categories_empty(self):
        response = self.client.get("/categories")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_category(self):
        category_data = {"name": "Category 1", "description": "Description 1"}
        response = self.client.post("/categories", json=category_data)
        self.assertEqual(response.status_code, 200)
        category = response.json()
        self.assertIsInstance(category, dict)
        self.assertEqual(category["name"], category_data["name"])
        self.assertEqual(category["description"], category_data["description"])

    def test_get_category(self):
        category_data = {"name": "Category 1", "description": "Description 1"}
        response = self.client.post("/categories", json=category_data)
        category = response.json()
        category_id = category["id"]
        response = self.client.get(f"/categories/{category_id}")
        self.assertEqual(response.status_code, 200)
        category = response.json()
        self.assertIsInstance(category, dict)
        self.assertEqual(category["name"], category_data["name"])
        self.assertEqual(category["description"], category_data["description"])

    def test_update_category(self):
        category_data = {"name": "Category 1", "description": "Description 1"}
        response = self.client.post("/categories", json=category_data)
        category = response.json()
        category_id = category["id"]
        update_data = {"name": "Category 1 Updated", "description": "Description 1 Updated"}
        response = self.client.put(f"/categories/{category_id}", json=update_data)
        self.assertEqual(response.status_code, 200)
        category = response.json()
        self.assertIsInstance(category, dict)
        self.assertEqual(category["name"], update_data["name"])
        self.assertEqual(category["description"], update_data["description"])

    def test_delete_category(self):
        category_data = {"name": "Category 1", "description": "Description 1"}
        response = self.client.post("/categories", json=category_data)
        category = response.json()
        category_id = category["id"]
        response = self.client.delete(f"/categories/{category_id}")
        self.assertEqual(response.status_code, 204)
        response = self.client.get(f"/categories/{category_id}")
        self.assertEqual(response.status_code, 404)
