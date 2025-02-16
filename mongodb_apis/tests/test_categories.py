
# -*- coding: utf-8 -*-

import os
import unittest
from fastapi.testclient import TestClient
from app.main import app
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ["MONGO_URI"])
db = client[os.environ["MONGO_DB_NAME_TEST"]]
collection = db["categories"]

class Category(BaseModel):
    id: int
    name: str
    description: str

class TestCategories(unittest.TestCase):

    def setUp(self):
        collection.delete_many({})

    def tearDown(self):
        collection.delete_many({})

    def test_create_category(self):
        data = {"name": "Category 1", "description": "Description 1"}
        response = TestClient(app).post("/categories/", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)

    def test_get_all_categories(self):
        data = [{"name": "Category 1", "description": "Description 1"}, {"name": "Category 2", "description": "Description 2"}]
        collection.insert_many(data)
        response = TestClient(app).get("/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)

    def test_get_category_by_id(self):
        data = {"name": "Category 1", "description": "Description 1"}
        collection.insert_one(data)
        response = TestClient(app).get("/categories/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), data)

    def test_update_category(self):
        data = {"name": "Category 1", "description": "Description 1"}
        collection.insert_one(data)
        new_data = {"name": "Category 1 Updated", "description": "Description 1 Updated"}
        response = TestClient(app).put("/categories/1", json=new_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), new_data)

    def test_delete_category(self):
        data = {"name": "Category 1", "description": "Description 1"}
        collection.insert_one(data)
        response = TestClient(app).delete("/categories/1")
        self.assertEqual(response.status_code, 204)

    def test_category_not_found(self):
        response = TestClient(app).get("/categories/1")
        self.assertEqual(response.status_code, 404)
