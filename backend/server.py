import os, uuid
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, ConfigDict
from starlette.middleware.cors import CORSMiddleware

ROOT_DIR=Path(__file__).parent
load_dotenv(ROOT_DIR/'.env')
memory_messages=[]
app=FastAPI(title='Padmraj Portfolio API')
api=APIRouter(prefix='/api')

class ContactCreate(BaseModel):
    name:str=Field(min_length=2,max_length=120)
    email:str=Field(min_length=5,max_length=160)
    subject:str=Field(min_length=2,max_length=200)
    message:str=Field(min_length=5,max_length=5000)

class ContactMessage(ContactCreate):
    model_config=ConfigDict(extra='ignore')
    id:str=Field(default_factory=lambda:str(uuid.uuid4()))
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))

@api.get('/')
async def root(): return {'message':'Padmraj Chougule - portfolio API running'}

@api.post('/contact',response_model=ContactMessage)
async def create_contact(payload:ContactCreate):
    if '@' not in payload.email or '.' not in payload.email.rsplit('@',1)[-1]: raise HTTPException(422,'Please provide a valid email address')
    item=ContactMessage(**payload.model_dump())
    stored=item.model_dump(); stored['created_at']=stored['created_at'].isoformat()
    memory_messages.insert(0,stored)
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        client=AsyncIOMotorClient(os.environ.get('MONGO_URL','mongodb://localhost:27017'),serverSelectionTimeoutMS=1000)
        await client[os.environ.get('DB_NAME','portfolio')].contact_messages.insert_one(stored)
    except Exception:
        pass
    return item

@api.get('/contact',response_model=list[ContactMessage])
async def get_contacts(limit:int=Query(20,ge=1,le=100)):
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        client=AsyncIOMotorClient(os.environ.get('MONGO_URL','mongodb://localhost:27017'),serverSelectionTimeoutMS=1000)
        docs=await client[os.environ.get('DB_NAME','portfolio')].contact_messages.find({},{'_id':0}).sort('created_at',-1).limit(limit).to_list(limit)
        out=[]
        for d in docs:
            if isinstance(d.get('created_at'),str): d['created_at']=datetime.fromisoformat(d['created_at'])
            out.append(ContactMessage(**d))
        return out
    except Exception:
        return [ContactMessage(**d) for d in memory_messages[:limit]]

app.include_router(api)
app.add_middleware(CORSMiddleware,allow_credentials=True,allow_origins=os.environ.get('CORS_ORIGINS','*').split(','),allow_methods=['*'],allow_headers=['*'])
