import streamlit as st
from PIL import Image
from core.ai_coach import iniciar_coach
from services.database import (
    iniciar_banco, obter_riot_id, salvar_riot_id,
    criar_nova_sessao, listar_sessoes, carregar_mensagens_sessao, 
    salvar_mensagem_sessao, deletar_sessao, atualizar_titulo_sessao
)
import os

# Configuração da página web
st.set_page_config(
    page_title="Coach - Valorant",
    page_icon="🎯",
    layout="centered"
)

# Estilização CSS personalizada (Dark Mode Gamer limpo)
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .stButton button {
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        border-color: #ff4655;
        color: #ff4655;
    }
    h1, h2, h3 {
        color: #ff4655 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    [data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 10px !important;
    }
    [data-testid="stFileUploader"] section {
        padding: 2px 8px !important;
        background-color: #161b22 !important;
        border: 1px dashed #ff4655 !important;
        border-radius: 8px;
        min-height: 45px;
    }
    [data-testid="stFileUploader"] section button {
        background-color: #ff4655 !important;
        color: white !important;
        border: none !important;
        padding: 2px 10px !important;
    }
    [data-testid="stFileUploader"] small {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa o banco de dados
iniciar_banco()

st.title("🎯 Coach - Valorant 🎯")
st.markdown("*O seu Head Coach particular de Valorant. Sem pano quente, foco em evolução pura.*")

# Verifica se o Riot ID está configurado
riot_id_salvo = obter_riot_id()

if not riot_id_salvo:
    st.warning("⚠️ Configuração pendente: Insira seu Riot ID para começar.")
    with st.form("form_riot_id"):
        input_id = st.text_input("Seu Riot ID (Ex: Chanáutico#CHANA):", placeholder="Nome#TAG")
        submit_button = st.form_submit_button("Conectar ao Servidor do Coach")
        
        if submit_button and input_id:
            if "#" in input_id:
                salvar_riot_id(input_id)
                st.success("Conectado com sucesso! Recarregando...")
                st.rerun()
            else:
                st.error("Formato inválido! O ID precisa conter '#' (Ex: Nome#TAG).")
    st.stop()

# Carrega sessões salvas para garantir o ID atual
sessoes_salvas = listar_sessoes()
if not sessoes_salvas:
    primeira_id = criar_nova_sessao("Análise Inicial")
    sessoes_salvas = listar_sessoes()

if "sessao_atual" not in st.session_state:
    st.session_state.sessao_atual = sessoes_salvas[0][0]

# Barra Lateral (Sidebar) limpa
with st.sidebar:
    st.markdown("### 🎮 Perfil Ativo")
    st.code(riot_id_salvo, language="text")
    
    if st.button("🔄 Trocar Riot ID"):
        salvar_riot_id("")
        st.rerun()
        
    st.markdown("---")
    st.subheader("💬 Histórico de Chats")
    
    if st.button("➕ Novo Chat"):
        nova_id = criar_nova_sessao("Nova Análise")
        st.session_state.sessao_atual = nova_id
        st.session_state.chat_session = iniciar_coach(riot_id_salvo)
        st.session_state.messages = []
        st.rerun()

    # Exibição limpa dos chats na barra lateral
    for s_id, s_titulo in sessoes_salvas:
        col_chat, col_del = st.columns([4, 1])
        with col_chat:
            label_botao = f"💬 {s_titulo}"
            if s_id == st.session_state.sessao_atual:
                label_botao = f"👉 {s_titulo}"
                
            if st.button(label_botao, key=f"sel_{s_id}"):
                st.session_state.sessao_atual = s_id
                st.session_state.chat_session = iniciar_coach(riot_id_salvo)
                mensagens_db = carregar_mensagens_sessao(s_id)
                st.session_state.messages = [{"role": "user" if r == "user" else "assistant", "content": c} for r, c in mensagens_db]
                st.rerun()
        with col_del:
            if st.button("🗑️", key=f"del_{s_id}"):
                deletar_sessao(s_id)
                st.rerun()

# Inicialização da sessão de chat na memória
if "chat_session" not in st.session_state:
    st.session_state.chat_session = iniciar_coach(riot_id_salvo)

if "messages" not in st.session_state:
    st.session_state.messages = []
    mensagens_db = carregar_mensagens_sessao(st.session_state.sessao_atual)
    for remetente, texto in mensagens_db:
        role = "user" if remetente == "user" else "assistant"
        st.session_state.messages.append({"role": role, "content": texto})

# Exibição das mensagens na tela principal
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Rodapé unificado (Uploader dinâmico com chave amarrada à sessão atual para limpar o arquivo ao trocar de chat)
st.markdown("---")
col_btn, col_txt = st.columns([1, 5])

with col_btn:
    # A key dinâmica garante que o uploader limpe o arquivo ao mudar de sessão
    arquivo_enviado = st.file_uploader(
        "Anexar", 
        type=["mp4", "mov", "avi", "mkv", "png", "jpg", "jpeg", "jxr", "mp3", "wav", "m4a"],
        label_visibility="collapsed",
        key=f"uploader_sessao_{st.session_state.sessao_atual}",
        help="Anexe vídeos, prints ou áudios (até 1.5GB)"
    )

with col_txt:
    prompt = st.chat_input("Mande sua dúvida, call ou feedback pro Coach...")

# O envio só acontece ao pressionar Enter / Enviar
if prompt:
    texto_usuario = prompt
    conteudo_para_ia = texto_usuario
    conteudo_para_historico = texto_usuario
    
    # Se for a primeira mensagem da sessão com título padrão, renomeia o chat automaticamente
    sessoes_atuais = listar_sessoes()
    for sid, stitulo in sessoes_atuais:
        if sid == st.session_state.sessao_atual and stitulo == "Nova Análise":
            novo_nome = (texto_usuario[:22] + '...') if len(texto_usuario) > 25 else texto_usuario
            atualizar_titulo_sessao(sid, novo_nome)
            break

    if arquivo_enviado:
        nome_arquivo = arquivo_enviado.name.lower()
        tamanho_bytes = arquivo_enviado.size
        limite_bytes = int(1.5 * 1024 * 1024 * 1024) # 1.5 GB
        
        if tamanho_bytes > limite_bytes:
            st.error("O arquivo ultrapassa o limite de 1,5 GB!")
        else:
            extensao_alvo = "jpg" if nome_arquivo.endswith(".jxr") else arquivo_enviado.name.split('.')[-1]
            temp_file_path = f"temp_upload_file.{extensao_alvo}"
            
            with open(temp_file_path, "wb") as f:
                f.write(arquivo_enviado.getbuffer())
                
            is_video = nome_arquivo.endswith((".mp4", ".mov", ".avi", ".mkv"))
            spinner_msg = "Enviando vídeo pesado para a IA..." if is_video else "Enviando arquivo para o Coach..."
            
            with st.spinner(spinner_msg):
                from google import genai
                client_upload = genai.Client()
                uploaded_file_ref = client_upload.files.upload(file=temp_file_path)
                
            conteudo_para_ia = [texto_usuario, uploaded_file_ref]
            
            if nome_arquivo.endswith((".jxr", ".png", ".jpg", ".jpeg")):
                conteudo_para_historico = f"{texto_usuario} [🖼️ Print/Imagem anexada]"
            elif nome_arquivo.endswith((".mp3", ".wav", ".m4a")):
                conteudo_para_historico = f"{texto_usuario} [🎙️ Áudio anexado]"
            else:
                conteudo_para_historico = f"{texto_usuario} [🎥 Vídeo anexado]"
                
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    st.session_state.messages.append({"role": "user", "content": conteudo_para_historico})
    with st.chat_message("user"):
        st.markdown(conteudo_para_historico)
            
    salvar_mensagem_sessao(st.session_state.sessao_atual, "user", conteudo_para_historico)

    with st.chat_message("assistant"):
        with st.spinner("O Coach tá analisando o material..."):
            try:
                response = st.session_state.chat_session.send_message(conteudo_para_ia)
                resposta_texto = response.text
                
                st.markdown(resposta_texto)
                st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
                salvar_mensagem_sessao(st.session_state.sessao_atual, "model", resposta_texto)
                
            except Exception as e:
                st.error(f"Erro ao processar arquivo com a IA: {e}")

                