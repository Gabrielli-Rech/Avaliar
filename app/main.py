from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scorezone.models import (
    Base,
    user,
    Categoria,
    Item,
    Avaliacao,
    Tag,
    ItemTag,
)

# ------------------- CONFIGURAÇÃO -------------------
DATABASE_URL = "mysql+pymysql://user:senha@localhost:3306/scorezone"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Cria todas as tabelas
Base.metadata.create_all(engine)

# ------------------- CRUD DE CATEGORIAS -------------------
def criar_categoria(nome):
    categoria = Categoria(nome=nome)
    session.add(categoria)
    session.commit()
    print(f"Categoria '{nome}' criada ✅")
    return categoria

def listar_categorias():
    return session.query(Categoria).all()

def atualizar_categoria(categoria_id, novo_nome):
    categoria = session.query(Categoria).get(categoria_id)
    if categoria:
        categoria.nome = novo_nome
        session.commit()
        print(f"Categoria atualizada para '{novo_nome}' ✅")
    else:
        print("Categoria não encontrada ❌")

def deletar_categoria(categoria_id):
    categoria = session.query(Categoria).get(categoria_id)
    if categoria:
        session.delete(categoria)
        session.commit()
        print(f"Categoria '{categoria.nome}' deletada ✅")
    else:
        print("Categoria não encontrada ❌")

# ------------------- CRUD DE ITENS -------------------
def criar_item(titulo, descricao, categoria):
    item = Item(titulo=titulo, descricao=descricao, categoria=categoria)
    session.add(item)
    session.commit()
    print(f"Item '{titulo}' criado ✅")
    return item

def listar_itens():
    return session.query(Item).all()

def atualizar_item(item_id, novo_titulo=None, nova_descricao=None):
    item = session.query(Item).get(item_id)
    if item:
        if novo_titulo: item.titulo = novo_titulo
        if nova_descricao: item.descricao = nova_descricao
        session.commit()
        print(f"Item '{item.titulo}' atualizado ✅")
    else:
        print("Item não encontrado ❌")

def deletar_item(item_id):
    item = session.query(Item).get(item_id)
    if item:
        session.delete(item)
        session.commit()
        print(f"Item '{item.titulo}' deletado ✅")
    else:
        print("Item não encontrado ❌")

# ------------------- CRUD DE USUÁRIOS -------------------
def criar_user(nome, email, senha):
    user = user(nome=nome, email=email, senha=senha)
    session.add(user)
    session.commit()
    print(f"Usuário '{nome}' criado ✅")
    return user

def listar_users():
    return session.query(user).all()

def atualizar_user(user_id, novo_nome=None, novo_email=None, nova_senha=None):
    user = session.query(user).get(user_id)
    if user:
        if novo_nome: user.nome = novo_nome
        if novo_email: user.email = novo_email
        if nova_senha: user.senha = nova_senha
        session.commit()
        print(f"Usuário '{user.nome}' atualizado ✅")
    else:
        print("Usuário não encontrado ❌")

def deletar_user(user_id):
    user = session.query(user).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        print(f"Usuário '{user.nome}' deletado ✅")
    else:
        print("Usuário não encontrado ❌")

# ------------------- CRUD DE AVALIAÇÕES -------------------
def criar_avaliacao(user, item, nota, comentario):
    avaliacao = Avaliacao(user=user, item=item, nota=nota, comentario=comentario)
    session.add(avaliacao)
    session.commit()
    print(f"Avaliação do item '{item.titulo}' criada ✅")
    return avaliacao

def listar_avaliacoes():
    return session.query(Avaliacao).all()

def atualizar_avaliacao(avaliacao_id, nova_nota=None, novo_comentario=None):
    avaliacao = session.query(Avaliacao).get(avaliacao_id)
    if avaliacao:
        if nova_nota: avaliacao.nota = nova_nota
        if novo_comentario: avaliacao.comentario = novo_comentario
        session.commit()
        print(f"Avaliação '{avaliacao.id}' atualizada ✅")
    else:
        print("Avaliação não encontrada ❌")

def deletar_avaliacao(avaliacao_id):
    avaliacao = session.query(Avaliacao).get(avaliacao_id)
    if avaliacao:
        session.delete(avaliacao)
        session.commit()
        print(f"Avaliação '{avaliacao.id}' deletada ✅")
    else:
        print("Avaliação não encontrada ❌")

# ------------------- FAVORITOS -------------------
def adicionar_favorito(user, item):
    user.favoritos.append(item)
    session.commit()
    print(f"{user.nome} favoritou {item.titulo} ✅")

def remover_favorito(user, item):
    if item in user.favoritos:
        user.favoritos.remove(item)
        session.commit()
        print(f"{item.titulo} removido dos favoritos de {user.nome} ✅")
    else:
        print("Item não está nos favoritos ❌")

# ------------------- TAGS -------------------
def criar_tag(nome):
    tag = Tag(nome=nome)
    session.add(tag)
    session.commit()
    print(f"Tag '{nome}' criada ✅")
    return tag

def adicionar_tag_item(item, tag):
    item.tags.append(tag)
    session.commit()
    print(f"Tag '{tag.nome}' adicionada ao item '{item.titulo}' ✅")

# ------------------- EXEMPLO DE USO -------------------
if __name__ == "__main__":
    # Criando categorias
    cat_jogos = criar_categoria("Jogos")
    cat_series = criar_categoria("Séries")

    # Criando itens
    item1 = criar_item("The Legend of Zelda", "Aventura épica", cat_jogos)
    item2 = criar_item("Stranger Things", "Série de suspense", cat_series)

    # Criando usuário
    user1 = criar_user("Gaybi", "gaybi@email.com", "123456")

    # Criando avaliações
    criar_avaliacao(user1, item1, 9.5, "Melhor jogo de todos!")
    criar_avaliacao(user1, item2, 8.0, "Muito bom, mas podia ter mais suspense.")

    # Favoritar item
    adicionar_favorito(user1, item2)

    # Criando tags
    tag_aventura = criar_tag("Aventura")
    tag_suspense = criar_tag("Suspense")

    # Adicionando tags aos itens
    adicionar_tag_item(item1, tag_aventura)
    adicionar_tag_item(item2, tag_suspense)

    # Listando avaliações do usuário
    print("\n--- Avaliações do usuário ---")
    for aval in user1.avaliacoes:
        print(f"{aval.item.titulo}: {aval.nota} - {aval.comentario}")

    # Listando favoritos do usuário
    print("\n--- Favoritos do usuário ---")
    for fav in user1.favoritos:
        print(fav.titulo)
