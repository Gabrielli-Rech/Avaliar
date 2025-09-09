from unittest.mock import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)            # Nome do usuário
    email = Column(String(100), unique=True, nullable=False)  # Email único
    senha = Column(String(255), nullable=False)          # Senha (hash de preferência)
    data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)  # Data de registro

    # RELACIONAMENTOS
    avaliacoes = relationship("Avaliacao", back_populates="usuario")   # Avaliações feitas
    favoritos = relationship("Item", secondary="favoritos", back_populates="usuarios_favoritos")  # Itens favoritados

    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome}', email='{self.email}')>"
