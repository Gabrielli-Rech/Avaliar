from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "itens"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)          # Nome do jogo, livro, filme, série
    descricao = Column(Text)                               # Resumo ou sinopse
    categoria_id = Column(Integer, ForeignKey("categorias.id"))  # Link para a categoria (Jogos, Filmes, etc)

    # RELACIONAMENTOS
    categoria = relationship("Categoria", back_populates="itens")  # Categoria do item
    avaliacoes = relationship("Avaliacao", back_populates="item")  # Avaliações recebidas
    usuarios_favoritos = relationship("Usuario", secondary="favoritos", back_populates="favoritos")  # Quem favoritou
    tags = relationship("Tag", secondary="item_tags", back_populates="itens")  # Tags relacionadas

    def __repr__(self):
        return f"<Item(id={self.id}, titulo='{self.titulo}', categoria='{self.categoria.nome if self.categoria else 'N/A'}')>"
