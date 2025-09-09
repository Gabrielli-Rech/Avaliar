# scorezone/controllers/item_controller.py

from scorezone.models import Session, Item, Categoria, Tag
from scorezone.controllers import Session as session_global

# Criar sessão
session = session_global

# ---------- CRIAR ITEM ----------
def criar_item(titulo, descricao, categoria):
    item = Item(titulo=titulo, descricao=descricao, categoria=categoria)
    session.add(item)
    session.commit()
    return item

# ---------- LISTAR ITENS ----------
def listar_itens():
    return session.query(Item).all()

# ---------- BUSCAR ITEM POR ID ----------
def get_item(item_id):
    item = session.query(Item).get(item_id)
    return item

# ---------- ATUALIZAR ITEM ----------
def atualizar_item(item_id, novo_titulo=None, nova_descricao=None, nova_categoria=None):
    item = session.query(Item).get(item_id)
    if not item:
        return None
    if novo_titulo:
        item.titulo = novo_titulo
    if nova_descricao:
        item.descricao = nova_descricao
    if nova_categoria:
        item.categoria = nova_categoria
    session.commit()
    return item

# ---------- DELETAR ITEM ----------
def deletar_item(item_id):
    item = session.query(Item).get(item_id)
    if not item:
        return False
    session.delete(item)
    session.commit()
    return True

# ---------- ADICIONAR TAG AO ITEM ----------
def adicionar_tag(item_id, tag):
    item = session.query(Item).get(item_id)
    if not item:
        return None
    item.tags.append(tag)
    session.commit()
    return item

# ---------- REMOVER TAG DO ITEM ----------
def remover_tag(item_id, tag):
    item = session.query(Item).get(item_id)
    if not item:
        return None
    if tag in item.tags:
        item.tags.remove(tag)
        session.commit()
    return item
