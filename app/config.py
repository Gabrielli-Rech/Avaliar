# scorezone/config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from scorezone.models import Base

# ---------- CONFIGURAÇÃO DO BANCO DE DADOS ----------
DB_USER = "root"
DB_PASSWORD = " "
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "scorezone"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ---------- ENGINE ----------
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

# ---------- SESSÃO ----------
Session = scoped_session(sessionmaker(bind=engine))

# ---------- FUNÇÃO PARA CRIAR TODAS AS TABELAS ----------
def init_db():
    Base.metadata.create_all(engine)
    print("✅ Todas as tabelas foram criadas com sucesso!")

# ---------- OUTRAS CONFIGURAÇÕES GERAIS ----------
SECRET_KEY = "scorezone_super_secreto"  # pra autenticação/Flask sessions
