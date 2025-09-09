# scorezone/controllers/auth_controller.py

from scorezone.models import Session, Usuario
from passlib.hash import bcrypt  # pra hashear senha de forma segura

# Criar sessão
session = Session()

# ---------- REGISTRO ----------
def registrar_usuario(nome, email, senha):
    # Checa se o email já existe
    usuario_existente = session.query(Usuario).filter_by(email=email).first()
    if usuario_existente:
        return {"erro": "Email já registrado!"}

    # Criptografa a senha
    senha_hash = bcrypt.hash(senha)

    # Cria usuário
    novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
    session.add(novo_usuario)
    session.commit()

    return {"sucesso": f"Usuário '{nome}' registrado com sucesso!"}

# ---------- LOGIN ----------
def login_usuario(email, senha):
    usuario = session.query(Usuario).filter_by(email=email).first()

    if not usuario:
        return {"erro": "Usuário não encontrado!"}

    # Verifica senha
    if bcrypt.verify(senha, usuario.senha):
        return {"sucesso": f"Bem-vindo {usuario.nome}!", "usuario_id": usuario.id}
    else:
        return {"erro": "Senha incorreta!"}

# ---------- GET USUÁRIO POR ID ----------
def get_usuario(usuario_id):
    usuario = session.query(Usuario).get(usuario_id)
    if usuario:
        return usuario
    return None
