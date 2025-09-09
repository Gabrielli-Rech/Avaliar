# scorezone/controllers/avaliacao_controller.py

from scorezone.models import Session, Avaliacao, Item, Usuario
from scorezone.controllers import Session as session_global

# Criar sessão
session = session_global

# ---------- CRIAR AVALIAÇÃO ----------
def criar_avaliacao(usuario, item, nota, comentario):
    avaliacao = Avaliacao(usuario=usuario, item=item, nota=nota, comentario=comentario)
    session.add(avaliacao)
    session.commit()
    return avaliacao

# ---------- LISTAR AVALIAÇÕES ----------
def listar_avaliacoes():
    return session.query(Avaliacao).all()

# ---------- BUSCAR AVALIAÇÃO POR ID ----------
def get_avaliacao(avaliacao_id):
    avaliacao = session.query(Avaliacao).get(avaliacao_id)
    return avaliacao

# ---------- ATUALIZAR AVALIAÇÃO ----------
def atualizar_avaliacao(avaliacao_id, nova_nota=None, novo_comentario=None):
    avaliacao = session.query(Avaliacao).get(avaliacao_id)
    if not avaliacao:
        return None
    if nova_nota:
        avaliacao.nota = nova_nota
    if novo_comentario:
        avaliacao.comentario = novo_comentario
    session.commit()
    return avaliacao

# ---------- DELETAR AVALIAÇÃO ----------
def deletar_avaliacao(avaliacao_id):
    avaliacao = session.query(Avaliacao).get(avaliacao_id)
    if not avaliacao:
        return False
    session.delete(avaliacao)
    session.commit()
    return True

# ---------- LISTAR AVALIAÇÕES POR ITEM ----------
def listar_avaliacoes_por_item(item_id):
    return session.query(Avaliacao).filter_by(item_id=item_id).all()

# ---------- CALCULAR MÉDIA DE UM ITEM ----------
def media_item(item_id):
    avaliacoes = session.query(Avaliacao).filter_by(item_id=item_id).all()
    if not avaliacoes:
        return 0
    soma = sum([a.nota for a in avaliacoes])
    media = soma / len(avaliacoes)
    return round(media, 2)
