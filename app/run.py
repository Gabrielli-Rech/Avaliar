from flask import Flask, request, jsonify
from scorezone.config import init_db, Session
from scorezone.controllers import (
    auth_controller,
    usuario_controller,
    item_controller,
    avaliacao_controller
)

# ---------- INICIAR APP ----------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'scorezone_super_secreto'
init_db()  # Cria tabelas se não existirem

# Sessão global
session = Session()

# ---------- ROTAS AUTH ----------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    resultado = auth_controller.registrar_usuario(
        nome=data.get('nome'),
        email=data.get('email'),
        senha=data.get('senha')
    )
    return jsonify(resultado)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    resultado = auth_controller.login_usuario(
        email=data.get('email'),
        senha=data.get('senha')
    )
    return jsonify(resultado)

# ---------- ROTAS USUÁRIO ----------
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = usuario_controller.listar_usuarios()
    return jsonify([{"id": u.id, "nome": u.nome, "email": u.email} for u in usuarios])

# ---------- ROTAS ITENS ----------
@app.route('/itens', methods=['GET'])
def get_itens():
    itens = item_controller.listar_itens()
    return jsonify([{"id": i.id, "titulo": i.titulo, "descricao": i.descricao, 
                    "categoria": i.categoria.nome if i.categoria else None} for i in itens])

@app.route('/itens', methods=['POST'])
def criar_item():
    data = request.json
    categoria = session.query(item_controller.session.query(item_controller.Categoria)).get(data.get('categoria_id'))
    item = item_controller.criar_item(data.get('titulo'), data.get('descricao'), categoria)
    return jsonify({"id": item.id, "titulo": item.titulo})

# ---------- ROTAS AVALIAÇÕES ----------
@app.route('/avaliacoes', methods=['POST'])
def criar_avaliacao():
    data = request.json
    usuario = session.query(auth_controller.get_usuario(data.get('usuario_id')))
    item = session.query(item_controller.get_item(data.get('item_id')))
    aval = avaliacao_controller.criar_avaliacao(usuario, item, data.get('nota'), data.get('comentario'))
    return jsonify({"id": aval.id, "nota": aval.nota, "comentario": aval.comentario})

@app.route('/avaliacoes/item/<int:item_id>', methods=['GET'])
def listar_avaliacoes_item(item_id):
    avals = avaliacao_controller.listar_avaliacoes_por_item(item_id)
    return jsonify([{"usuario": a.usuario.nome, "nota": a.nota, "comentario": a.comentario} for a in avals])

# ---------- RUN SERVER ----------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
