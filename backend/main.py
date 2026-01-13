# main.py
from typing import List
import hashlib
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, JSON, select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("POSTGRES_CONNECTION_STRING")

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Database Model
class SchemaModel(Base):
    __tablename__ = "schemas"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    data = Column(JSON, nullable=False)
    hash = Column(String, nullable=False, unique=True)


# Pydantic Models
class SchemaCreate(BaseModel):
    title: str = Field(..., example="User Profile")
    data: dict = Field(..., example={"name": "Alice", "age": 30})

class SchemaListItem(BaseModel):
    id: int
    title: str
    hash: str

    class Config:
        orm_mode = True

class SchemaDetail(SchemaListItem):
    data: dict

    class Config:
        orm_mode = True


# FastAPI App
app = FastAPI(title="JSON Schema Storage API", version="1.0.0")


# Dependency
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# Create tables on startup
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# POST endpoint to save JSON schema
@app.post("/schemas/", response_model=SchemaListItem, summary="Create a new JSON schema")
async def create_schema(schema: SchemaCreate, session: AsyncSession = next(get_session())):
    # Calculate SHA256 hash of JSON data (sorted keys for consistency)
    json_bytes = json.dumps(schema.data, sort_keys=True).encode("utf-8")
    hash_value = hashlib.sha256(json_bytes).hexdigest()

    db_schema = SchemaModel(title=schema.title, data=schema.data, hash=hash_value)
    session.add(db_schema)
    try:
        await session.commit()
        await session.refresh(db_schema)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
    return db_schema


# GET endpoint to list all schemas (without JSON data)
@app.get("/schemas/", response_model=List[SchemaListItem], summary="List all schemas")
async def list_schemas(session: AsyncSession = next(get_session())):
    result = await session.execute(select(SchemaModel.id, SchemaModel.title, SchemaModel.hash))
    schemas = result.all()
    return [SchemaListItem(id=row.id, title=row.title, hash=row.hash) for row in schemas]


# GET endpoint to fetch full JSON by ID
@app.get("/schemas/{schema_id}", response_model=SchemaDetail, summary="Get schema details by ID")
async def get_schema(schema_id: int, session: AsyncSession = next(get_session())):
    result = await session.execute(select(SchemaModel).where(SchemaModel.id == schema_id))
    schema = result.scalar_one_or_none()
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")
    return schema
