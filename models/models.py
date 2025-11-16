from sqlmodel import SQLModel, Field

class Usuari(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password_hash: str
    email: str

class UsuariRequest(SQLModel):
    username: str
    password: str
    email: str

class UsuariResponse(SQLModel):
    id: int
    username: str
    email: str

class Tasca(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    usuari_id: int
    titol: str
    descripcio: str
    completada: bool = False

class TascaRequest(SQLModel):
    titol: str
    descripcio: str

class TascaResponse(SQLModel):
    id: int
    titol: str
    descripcio: str
    completada: bool

class TascaUpdate(SQLModel):
    completada: bool

class LoginRequest(SQLModel):
    username: str
    password: str