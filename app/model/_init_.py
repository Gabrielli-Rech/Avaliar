# scorezone/models/__init__.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

# Base do SQLAlchemy
Base = declarative_base()

# Importando os models
from .user import user
from .categoria import Categoria
from .item import Item
from .avaliacao import Avaliacao
from .tag import Tag, ItemTag  # Se você tiver implementado tags

# Criar engine (substitua os valores pelo seu MySQL)
DATABASE_URL = "mysql+pymysql://user:senha@localhost:3306/scorezone"
engine = create_engine(DATABASE_URL, echo=True)

# Criar sessão
Session = scoped_session(sessionmaker(bind=engine))

# Função para criar todas as tabelas
def init_db():
    Base.metadata.create_all(engine)
    print("✅ Todas as tabelas foram criadas com sucesso!")
