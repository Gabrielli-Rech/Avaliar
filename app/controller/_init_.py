# scorezone/controllers/__init__.py

from scorezone.models import (
    Session,
    user,
    Categoria,
    Item,
    Avaliacao,
    Tag
)

# Criar sessão global
session = Session()

# ---------- USUÁRIO ----------
def criar_user(nome, email, senha):
    from scorezone.main import criar_user as crud_criar_user
    return crud_criar_user(nome, email, senha)

def listar_users():
    from scorezone.main import listar_users as crud_listar_users
    return crud_listar_users()

# ---------- CATEGORIA ----------
def criar_categoria(nome):
    from scorezone.main import criar_categoria as crud_criar_categoria
    return crud_criar_categoria(nome)

def listar_categorias():
    from scorezone.main import listar_categorias as crud_listar_categorias
    return crud_listar_categorias()

# ---------- ITEM ----------
def criar_item(titulo, descricao, categoria):
    from scorezone.main import criar_item as crud_criar_item
    return crud_criar_item(titulo, descricao, categoria)

def listar_itens():
    from scorezone.main import listar_itens as crud_listar_itens
    return crud_listar_itens()

# ---------- AVALIAÇÃO ----------
def criar_avaliacao(user, item, nota, comentario):
    from scorezone.main import criar_avaliacao as crud_criar_avaliacao
    return crud_criar_avaliacao(user, item, nota, comentario)

def listar_avaliacoes():
    from scorezone.main import listar_avaliacoes as crud_listar_avaliacoes
    return crud_listar_avaliacoes()

# ---------- FAVORITOS ----------
def adicionar_favorito(user, item):
    from scorezone.main import adicionar_favorito as crud_adicionar_favorito
    return crud_adicionar_favorito(user, item)

def remover_favorito(user, item):
    from scorezone.main import remover_favorito as crud_remover_favorito
    return crud_remover_favorito(user, item)

# ---------- TAGS ----------
def criar_tag(nome):
    from scorezone.main import criar_tag as crud_criar_tag
    return crud_criar_tag(nome)

def adicionar_tag_item(item, tag):
    from scorezone.main import adicionar_tag_item as crud_adicionar_tag
    return crud_adicionar_tag(item, tag)
