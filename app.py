import sqlite3
import datetime
import time
import logging

# Conectar ao banco e criar tabela se nao existir
def conectar_banco():
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        data_validade TEXT,
        descricao TEXT,
        status TEXT DEFAULT 'ativo'
    )
    ''')
    conn.commit()
    return conn, cursor

conn, cursor = conectar_banco()

# Configurar log
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Validar data
def validar_data(data):
    if data == '':
        return True
    if '/' in data:
        print("Erro: Use '-' em vez de '/' para separar ano, mês e dia.")
        return False
    try:
        ano, mes, dia = map(int, data.split('-'))
        if not (1 <= mes <= 12):
            print("Erro: O mês deve estar entre 01 e 12.")
            return False
        if not (1 <= dia <= 31):
            print("Erro: O dia deve estar entre 01 e 31.")
            return False
        data_formatada = datetime.date(ano, mes, dia)
        if data_formatada < datetime.date.today():
            print("Erro: A data de validade não pode ser anterior à data atual.")
            return False
        return True
    except ValueError:
        print("Data inválida! Certifique-se de usar o formato AAAA-MM-DD com valores corretos.")
        return False

# Validar preco
def validar_preco(preco):
    try:
        preco = float(preco)
        if preco <= 0:
            raise ValueError
        return preco
    except ValueError:
        return None

# Validar id
def validar_id(id_input):
    if not id_input.isdigit() or int(id_input) <= 0:
        logging.warning("Tentativa de usar ID inválido.")
        print("ID inválido! Digite apenas números inteiros positivos.")
        return None
    return int(id_input)

# Listar produtos
def listar_produtos():
    cursor.execute("SELECT * FROM produto WHERE status = 'ativo'")
    produtos = cursor.fetchall()
    if produtos:
        print("\n--- Lista de Produtos ---")
        for produto in produtos:
            preco_formatado = f"R$ {produto[2]:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
            print(f"ID: {produto[0]} | Nome: {produto[1]} | Preço: {preco_formatado} | Validade: {produto[3] if produto[3] else 'N/A'} | Descrição: {produto[4] if produto[4] else 'N/A'}")
        print(f"\n✅ Total de produtos ativos: {len(produtos)}")
    else:
        print("Nenhum produto encontrado.")
    time.sleep(2)

# Buscar produto
def buscar_produto():
    id_busca = input("Digite o ID do produto que deseja buscar: ").strip()
    id_valido = validar_id(id_busca)
    if id_valido is None:
        return
    cursor.execute("SELECT * FROM produto WHERE id = ? AND status = 'ativo'", (id_valido,))
    produto = cursor.fetchone()
    if produto:
        preco_formatado = f"R$ {produto[2]:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        print(f"ID: {produto[0]} | Nome: {produto[1]} | Preço: {preco_formatado} | Validade: {produto[3] if produto[3] else 'N/A'} | Descrição: {produto[4] if produto[4] else 'N/A'}")
    else:
        print("Produto não encontrado.")
    time.sleep(2)

# Adicionar produto
def adicionar_produto():
    print("\n--- Cadastro de Produto ---")
    nome = input("Nome do produto: ").strip()
    while not nome:
        print("Nome é obrigatório!")
        nome = input("Nome do produto: ").strip()

    cursor.execute("SELECT * FROM produto WHERE nome = ? AND status = 'ativo'", (nome,))
    produto_existente = cursor.fetchone()
    if produto_existente:
        print("\nJá existe um produto com esse nome cadastrado.")
        confirmar = input("Deseja continuar mesmo assim? (s/n): ").strip().lower()
        if confirmar != 's':
            print("Cadastro cancelado.")
            time.sleep(2)
            return

    preco = None
    while preco is None:
        preco_input = input("Preço do produto: ").strip()
        preco = validar_preco(preco_input)
        if preco is None:
            print("Preço inválido! Digite um valor numérico positivo.")

    data_validade = input("Data de validade (opcional, formato AAAA-MM-DD): ").strip()
    while not validar_data(data_validade):
        data_validade = input("Data de validade (opcional, formato AAAA-MM-DD): ").strip()

    descricao = input("Descrição (opcional): ").strip()

    cursor.execute(
        "INSERT INTO produto (nome, preco, data_validade, descricao) VALUES (?, ?, ?, ?)",
        (nome, preco, data_validade if data_validade else None, descricao if descricao else None)
    )
    conn.commit()
    logging.info(f"Produto cadastrado: {nome}")
    print("✅ Produto cadastrado com sucesso!")
    time.sleep(2)

# Atualizar produto
def atualizar_produto():
    print("\n--- Atualizar Produto ---")
    id_update = input("ID do produto a atualizar: ").strip()
    id_valido = validar_id(id_update)
    if id_valido is None:
        return

    cursor.execute("SELECT * FROM produto WHERE id = ? AND status = 'ativo'", (id_valido,))
    produto_atual = cursor.fetchone()
    if not produto_atual:
        print("Produto não encontrado.")
        time.sleep(2)
        return

    nome = input("Novo nome do produto: ").strip()
    while not nome:
        print("Nome é obrigatório!")
        nome = input("Novo nome do produto: ").strip()

    preco = None
    while preco is None:
        preco_input = input("Novo preço do produto: ").strip()
        preco = validar_preco(preco_input)
        if preco is None:
            print("Preço inválido! Digite um valor numérico positivo.")

    data_validade = input("Nova data de validade (opcional, formato AAAA-MM-DD): ").strip()
    while not validar_data(data_validade):
        data_validade = input("Nova data de validade (opcional, formato AAAA-MM-DD): ").strip()

    descricao = input("Nova descrição (opcional): ").strip()

    cursor.execute(
        "UPDATE produto SET nome = ?, preco = ?, data_validade = ?, descricao = ? WHERE id = ?",
        (nome, preco, data_validade if data_validade else None, descricao if descricao else None, id_valido)
    )
    conn.commit()
    logging.info(f"Produto atualizado: ID {id_valido}")
    print("✅ Produto atualizado com sucesso!")
    time.sleep(2)

# Deletar produto (soft delete)
def deletar_produto():
    id_delete = input("Digite o ID do produto que deseja deletar: ").strip()
    id_valido = validar_id(id_delete)
    if id_valido is None:
        return

    cursor.execute("SELECT * FROM produto WHERE id = ? AND status = 'ativo'", (id_valido,))
    produto = cursor.fetchone()

    if produto:
        preco_formatado = f"R$ {produto[2]:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
        print(f"Produto encontrado:\nID: {produto[0]} | Nome: {produto[1]} | Preço: {preco_formatado}")
        confirmacao = input("Tem certeza que deseja deletar este produto? (s/n): ").strip().lower()
        if confirmacao == 's':
            cursor.execute("UPDATE produto SET status = 'inativo' WHERE id = ?", (id_valido,))
            conn.commit()
            logging.info(f"Produto marcado como inativo: ID {id_valido}")
            print("✅ Produto marcado como inativo!")
        else:
            print("Operação cancelada.")
    else:
        print("Produto não encontrado.")
    time.sleep(2)

# Menu
def menu():
    while True:
        print("\n--- MENU CRUD PRODUTOS ---")
        print("1 - Listar Produtos")
        print("2 - Buscar Produto por ID")
        print("3 - Adicionar Produto")
        print("4 - Atualizar Produto")
        print("5 - Deletar Produto")
        print("6 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_produtos()
        elif opcao == "2":
            buscar_produto()
        elif opcao == "3":
            adicionar_produto()
        elif opcao == "4":
            atualizar_produto()
        elif opcao == "5":
            deletar_produto()
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
    conn.close()
