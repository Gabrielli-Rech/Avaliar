# scorezone/controllers/usuario_controller.py

from scorezone.models import Session, Usuario, Item
from scorezone.controllers import Session as session_global

# Criar sessão
session = session_global

# ---------- CRIAR USUÁRIO ----------
def criar_usuario(nome, email, senha_hash=None):
    usuario = Usuario(nome=nome, email=email, senha=senha_hash if senha_hash else "")
    session.add(usuario)
    session.commit()
    return usuario

# ---------- LISTAR USUÁRIOS ----------
def listar_usuarios():
    return session.query(Usuario).all()

# ---------- BUSCAR USUÁRIO POR ID ----------
def get_usuario(usuario_id):
    usuario = session.query(Usuario).get(usuario_id)
    return usuario

# ---------- ATUALIZAR USUÁRIO ----------
def atualizar_usuario(usuario_id, novo_nome=None, novo_email=None, nova_senha=None):
    usuario = session.query(Usuario).get(usuario_id)
    if not usuario:
        return None
    if novo_nome:
        usuario.nome = novo_nome
    if novo_email:
        usuario.email = novo_email
    if nova_senha:
        usuario.senha = nova_senha
    session.commit()
    return usuario

# ---------- DELETAR USUÁRIO ----------
def deletar_usuario(usuario_id):
    usuario = session.query(Usuario).get(usuario_id)
    if not usuario:
        return False
    session.delete(usuario)
    session.commit()
    return True

# ---------- GERENCIAR FAVORITOS ----------
def adicionar_favorito(usuario, item):
    if item not in usuario.favoritos:
        usuario.favoritos.append(item)
        session.commit()
    return usuario

def remover_favorito(usuario, item):
    if item in usuario.favoritos:
        usuario.favoritos.remove(item)
        session.commit()
    return usuario

def listar_favoritos(usuario):
    return usuario.favoritos if usuario else []
