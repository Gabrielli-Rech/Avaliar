from unittest.mock import Base
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # Quem avaliou
    item_id = Column(Integer, ForeignKey("itens.id"), nullable=False)       # Sobre qual Item
    nota = Column(Float, nullable=False)                                     # Nota do usuário (ex: 8.5)
    comentario = Column(Text)                                                # Comentário textual
    data = Column(DateTime, default=datetime.datetime.utcnow)                # Data da avaliação

    # RELACIONAMENTOS
    usuario = relationship("Usuario", back_populates="avaliacoes")           # Conecta ao usuário
    item = relationship("Item", back_populates="avaliacoes")                 # Conecta ao Item

    def __repr__(self):
        return f"<Avaliacao(id={self.id}, usuario_id={self.usuario_id}, item_id={self.item_id}, nota={self.nota})>"
