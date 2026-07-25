import os
from google import genai
import time
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

def processar_vod(caminho_video):
    print(f"\n[Sistema] Subindo o seu VOD ({caminho_video}) pro Coach Frttt analisar...")
    print("[Sistema] Ele tá pegando o caderninho, peraí", end="")
    
    # Upload usando a nova biblioteca oficial
    video_file = client.files.upload(file=caminho_video)
    
    # Aguarda o processamento ficar ativo
    while video_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)
        
    if video_file.state.name == "FAILED":
        raise ValueError("\n[Erro] Oxe, deu ruim no processamento do vídeo. Vê se o formato tá certo (MP4).")
        
    print("\n[Sistema] Vídeo processado! O Coach tá pronto pra te esculachar.")
    return video_file