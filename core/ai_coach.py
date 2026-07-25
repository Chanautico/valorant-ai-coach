import os
from google import genai
from dotenv import load_dotenv
from services.tracker_api import buscar_dados_tracker

# Carrega o .env apenas se ele existir localmente (na nuvem usamos os Secrets do Streamlit)
if os.path.exists(".env"):
    load_dotenv()

client = genai.Client()

def iniciar_coach(riot_id):
    relatorio_stats = buscar_dados_tracker(riot_id)
    
    instrucoes_coach = f"""
    Você é um Head Coach de Valorant de nível Radiante e ex-pro player. Sua personalidade é intensa, enérgica, extremamente detalhista e exigente, inspirado no estilo de análise do streamer 'frttt'. 

    DADOS ATUAIS DO ALUNO:
    {relatorio_stats}

    DIRETRIZES DE TREINAMENTO E VÍDEOS:
    - Analise posicionamento, mira, economia e utilitárias sem passar pano para bagre.
    - QUANDO O ALUNO APRESENTAR ERROS TÉCNICOS GRAVES (ex: mira no chão, movimentação errada, falha em retake), INDIQUE VÍDEOS DE TREINAMENTO REAIS DO YOUTUBE (como guias de ProGuides, Woohoojin, Sova, Casters ou tutoriais específicos de mira/macro). Insira o link markdown ou o nome exato do canal/vídeo para ele pesquisar e treinar.
    - Você aceita imagens, áudios e vídeos enviados pelo aluno para analisar prints de partida ou gravações completas de gameplay.
    """
    
    # Rota atualizada para os modelos estáveis mais recentes da API do Gemini
    modelos_disponiveis = [
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash"
    ]
    
    chat = None
    ultimo_erro = None
    
    for nome_modelo in modelos_disponiveis:
        try:
            chat = client.chats.create(
                model=nome_modelo,
                config={"system_instruction": instrucoes_coach}
            )
            break
        except Exception as e:
            ultimo_erro = e
            continue
            
    if not chat:
        raise Exception(f"Erro ao inicializar as rotas da IA. Último erro: {ultimo_erro}")
        
    return chat