from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
from typing import List
import os
from models.models import Usuari, UsuariRequest, UsuariResponse, Tasca, TascaRequest, TascaResponse, TascaUpdate, LoginRequest

app = FastAPI()

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()



@app.post("/api/login", response_model=UsuariResponse, tags=["Autenticació"])
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(Usuari).where(Usuari.username == login_data.username)
    usuari = db.exec(stmt).first()
    return usuari


@app.post("/api/register", response_model=UsuariResponse, tags=["Autenticació"])
def register(usuari: UsuariRequest, db: Session = Depends(get_db)):
    nou_usuari = Usuari(
        username=usuari.username,
        password_hash=usuari.password,
        email=usuari.email
    )
    db.add(nou_usuari)
    db.commit()
    return nou_usuari


@app.get("/api/tasques", response_model=List[TascaResponse], tags=["Tasques"])
def obtenir_tasques(usuari_id: int, db: Session = Depends(get_db)):
    stmt = select(Tasca).where(Tasca.usuari_id == usuari_id)
    tasques = db.exec(stmt).all()
    return tasques


@app.post("/api/tasques", response_model=TascaResponse, tags=["Tasques"])
def crear_tasca(tasca: TascaRequest, usuari_id: int, db: Session = Depends(get_db)):
    nova_tasca = Tasca(
        usuari_id=usuari_id,
        titol=tasca.titol,
        descripcio=tasca.descripcio
    )
    db.add(nova_tasca)
    db.commit()
    return nova_tasca


@app.patch("/api/tasques/{tasca_id}/completar", response_model=TascaResponse, tags=["Tasques"])
def completar_tasca(tasca_id: int, tasca_update: TascaUpdate, db: Session = Depends(get_db)):
    stmt = select(Tasca).where(Tasca.id == tasca_id)
    tasca = db.exec(stmt).first()
    tasca.completada = tasca_update.completada
    db.add(tasca)
    db.commit()
    return tasca


@app.delete("/api/tasques/{tasca_id}", response_model=dict, tags=["Tasques"])
def eliminar_tasca(tasca_id: int, db: Session = Depends(get_db)):
    stmt = select(Tasca).where(Tasca.id == tasca_id)
    tasca = db.exec(stmt).first()
    db.delete(tasca)
    db.commit()
    return {"msg": "Tasca eliminada correctament"}