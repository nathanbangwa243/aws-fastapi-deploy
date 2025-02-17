
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import Field, BaseModel, validator, ConfigDict
from typing import List, Optional
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure

router = APIRouter(prefix="/categories", tags=["categories"])


class Category(BaseModel):
    id: int = Field(..., alias="_id", description="Category ID")
    name: str
    description: Optional[str] = None

    class Config(ConfigDict):
        allow_population_by_field_name = True


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


@router.get("/", response_model=List[Category])
async def get_categories(db=Depends(get_db)):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    try:
        categories = list(db.categories.find())
        return categories
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status_code, detail=str(e))


@router.post("/", response_model=Category)
async def create_category(category: CategoryCreate, db=Depends(get_db)):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    try:
        category_id = db.categories.insert_one(category.dict()).inserted_id
        category.id = category_id
        return category
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status_code, detail=str(e))


@router.get("/{category_id}", response_model=Category)
async def get_category(category_id: int, db=Depends(get_db)):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    try:
        category = db.categories.find_one({"_id": category_id})
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        return category
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status_code, detail=str(e))


@router.put("/{category_id}", response_model=Category)
async def update_category(category_id: int, category: CategoryUpdate, db=Depends(get_db)):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    try:
        db.categories.update_one({"_id": category_id}, {"$set": category.dict()})
        category.id = category_id
        return category
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status_code, detail=str(e))


@router.delete("/{category_id}")
async def delete_category(category_id: int, db=Depends(get_db)):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    try:
        db.categories.delete_one({"_id": category_id})
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(status_code=status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status_code, detail=str(e))


def get_db():
    try:
        client = MongoClient(os.environ["MONGO_URI"])
        db = client[os.environ["MONGO_DB_NAME"]]
        return db
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
