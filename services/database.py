import sqlite3

DB_NAME = "banco_coach.db"

def iniciar_banco():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracoes (
            chave TEXT PRIMARY KEY,
            valor TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sessao_id INTEGER,
            remetente TEXT,
            conteudo TEXT,
            FOREIGN KEY (sessao_id) REFERENCES sessoes (id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def obter_riot_id():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT valor FROM configuracoes WHERE chave = 'riot_id'")
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def salvar_riot_id(riot_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO configuracoes (chave, valor) VALUES ('riot_id', ?)", (riot_id,))
    conn.commit()
    conn.close()

def criar_nova_sessao(titulo="Nova Conversa"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessoes (titulo) VALUES (?)", (titulo,))
    sessao_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return sessao_id

def atualizar_titulo_sessao(sessao_id, novo_titulo):
    """Atualiza o título do chat dinamicamente com base na primeira mensagem do usuário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE sessoes SET titulo = ? WHERE id = ?", (novo_titulo, sessao_id))
    conn.commit()
    conn.close()

def listar_sessoes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo FROM sessoes ORDER BY id DESC")
    sessoes = cursor.fetchall()
    conn.close()
    return sessoes

def carregar_mensagens_sessao(sessao_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT remetente, conteudo FROM mensagens WHERE sessao_id = ?", (sessao_id,))
    mensagens = cursor.fetchall()
    conn.close()
    return mensagens

def salvar_mensagem_sessao(sessao_id, remetente, conteudo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mensagens (sessao_id, remetente, conteudo) VALUES (?, ?, ?)", (sessao_id, remetente, conteudo))
    conn.commit()
    conn.close()

def deletar_sessao(sessao_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mensagens WHERE sessao_id = ?", (sessao_id,))
    cursor.execute("DELETE FROM sessoes WHERE id = ?", (sessao_id,))
    conn.commit()
    conn.close()