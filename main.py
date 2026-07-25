import os
from google import genai
from dotenv import load_dotenv

# 1. Abre o cofre e pega a chave VIP
load_dotenv()
CHAVE_API = os.getenv("GEMINI_API_KEY")

# 2. Configura o motor NOVO da IA
client = genai.Client(api_key=CHAVE_API)

# 3. O nosso Prompt Master
prompt_sistema = """Você é o maior especialista em treinamento competitivo de VALORANT do mundo. 
Seu objetivo é maximizar a evolução do jogador. Seja exigente e identifique os erros."""

# 4. A mensagem do jogador
mensagem_usuario = "Sou ferro, jogo de Sage, Killjoy e Breach e pino tiro demais. O que eu faço pra começar a melhorar?"

print("Pensando na jogada... aguarde!\n")

# 5. A IA processa tudo e responde (usando a sintaxe nova)
resposta = client.models.generate_content(
    model='gemini-flash-latest',
    contents=f"{prompt_sistema}\n\nJogador: {mensagem_usuario}"
)

print("--- RESPOSTA DO HEAD COACH ---")
print(resposta.text)