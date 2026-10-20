import json
import os
from pathlib import Path
from typing import Any
from fastapi import Depends, FastAPI, Header, HTTPException, Query, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from sqlalchemy import JSON, Boolean, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

ROOT = Path(__file__).resolve().parents[2]
DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{ROOT / "offlinemock.db"}')
engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
class Base(DeclarativeBase): pass
class PackRecord(Base):
    __tablename__ = 'packs'
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    title: Mapped[str] = mapped_column(String(160))
    subject: Mapped[str] = mapped_column(String(80))
    level: Mapped[str] = mapped_column(String(80))
    topic: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    estimated_minutes: Mapped[int] = mapped_column(Integer)
    language: Mapped[str] = mapped_column(String(120))
    questions: Mapped[list[dict[str, Any]]] = mapped_column(JSON)
    published: Mapped[bool] = mapped_column(Boolean, default=False)

class Pack(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(min_length=1, max_length=100)
    version: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=160)
    subject: str = Field(min_length=1, max_length=80)
    level: str = Field(min_length=1, max_length=80)
    topic: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=1000)
    estimatedMinutes: int = Field(gt=0, le=600)
    language: str = Field(min_length=1, max_length=120)
    questions: list[dict[str, Any]] = Field(min_length=1, max_length=100)
class PublishPack(Pack): published: bool = True

def require_teacher(x_teacher_key: str | None = Header(default=None)):
    expected = os.getenv('TEACHER_API_KEY')
    if not expected or x_teacher_key != expected: raise HTTPException(status_code=401, detail='Teacher authentication required')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def record_to_pack(record: PackRecord) -> dict[str, Any]: return {'id': record.id, 'version': record.version, 'title': record.title, 'subject': record.subject, 'level': record.level, 'topic': record.topic, 'description': record.description, 'estimatedMinutes': record.estimated_minutes, 'language': record.language, 'questions': record.questions}
def seed(db: Session):
    if db.scalar(select(PackRecord.id).limit(1)): return
    source = ROOT / 'content' / 'packs'
    for file in source.glob('*.json'):
        data = json.loads(file.read_text())
        db.add(PackRecord(id=data['id'], version=data['version'], title=data['title'], subject=data['subject'], level=data['level'], topic=data['topic'], description=data['description'], estimated_minutes=data['estimatedMinutes'], language=data['language'], questions=data['questions'], published=True))
    db.commit()
Base.metadata.create_all(engine)
with SessionLocal() as db: seed(db)
app = FastAPI(title='OfflineMock API', version='1.0.0')
origins = [value.strip() for value in os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=['*'], allow_headers=['*'])
@app.get('/health')
def health(): return {'status': 'ok', 'service': 'offlinemock-api'}
@app.get('/api/v1/packs')
def list_packs(q: str | None = Query(default=None), limit: int = Query(default=50, le=100), db: Session = Depends(get_db)):
    records = db.scalars(select(PackRecord).where(PackRecord.published.is_(True)).limit(limit)).all()
    return [record_to_pack(r) for r in records if not q or q.lower() in f'{r.title} {r.subject} {r.topic}'.lower()]
@app.get('/api/v1/packs/{pack_id}')
def get_pack(pack_id: str, db: Session = Depends(get_db)):
    record = db.get(PackRecord, pack_id)
    if not record or not record.published: raise HTTPException(404, 'Pack not found')
    return record_to_pack(record)
@app.get('/api/v1/packs/{pack_id}/download')
def download_pack(pack_id: str, db: Session = Depends(get_db)):
    record = db.get(PackRecord, pack_id)
    if not record or not record.published: raise HTTPException(404, 'Pack not found')
    return Response(content=json.dumps(record_to_pack(record)), media_type='application/json', headers={'Content-Disposition': f'attachment; filename="{record.id}.json"'})
@app.post('/api/v1/packs', dependencies=[Depends(require_teacher)], status_code=status.HTTP_201_CREATED)
def create_pack(pack: Pack, db: Session = Depends(get_db)):
    if db.get(PackRecord, pack.id): raise HTTPException(409, 'Pack id already exists')
    record = PackRecord(id=pack.id, version=pack.version, title=pack.title, subject=pack.subject, level=pack.level, topic=pack.topic, description=pack.description, estimated_minutes=pack.estimatedMinutes, language=pack.language, questions=pack.questions, published=False)
    db.add(record); db.commit(); return record_to_pack(record)
@app.put('/api/v1/packs/{pack_id}', dependencies=[Depends(require_teacher)])
def update_pack(pack_id: str, pack: Pack, db: Session = Depends(get_db)):
    record = db.get(PackRecord, pack_id)
    if not record: raise HTTPException(404, 'Pack not found')
    for key, value in record_to_pack(record).items():
        if key != 'id': setattr(record, {'estimatedMinutes':'estimated_minutes'}.get(key, key), getattr(pack, key))
    db.commit(); return record_to_pack(record)
@app.delete('/api/v1/packs/{pack_id}', dependencies=[Depends(require_teacher)], status_code=204)
def delete_pack(pack_id: str, db: Session = Depends(get_db)):
    record = db.get(PackRecord, pack_id)
    if not record: raise HTTPException(404, 'Pack not found')
    db.delete(record); db.commit()
@app.post('/api/v1/packs/import', dependencies=[Depends(require_teacher)], status_code=201)
def import_pack(pack: Pack, db: Session = Depends(get_db)): return create_pack(pack, db)
