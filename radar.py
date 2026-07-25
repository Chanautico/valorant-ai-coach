import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
CHAVE = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=CHAVE)

print("Passando o radar no Google...\n")

try:
    # Vasculha o servidor pra ver a lista VIP
    for m in client.models.list():
        print(f"- {m.name}")
except Exception as e:
    print(f"Deu ruim no radar: {e}")