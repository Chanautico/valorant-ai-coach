from core.ai_coach import iniciar_coach
from services.database import iniciar_banco, salvar_mensagem
# Importando nossa nova ferramenta de vídeo!
from services.video_handler import processar_vod 

def main():
    print("Iniciando o sistema...")
    iniciar_banco()
    chat = iniciar_coach()
    
    print("Coach Frttt da Shopee tá online. Digite 'sair' para quitar.")
    print("🎬 DICA: Para analisar uma play, digite: /video caminho/do/arquivo.mp4\n")

    while True:
        mensagem = input("Você: ")
        
        if mensagem.lower() == 'sair':
            print("Coach: Vai lá, seu bagre. Vê se treina pelo menos no The Range!")
            break
            
        # 1. IDENTIFICANDO O MODO VÍDEO
        if mensagem.lower().startswith("/video"):
            # Picota a string pra pegar só o que vem depois do espaço
            partes = mensagem.split(" ", 1)
            
            if len(partes) < 2:
                print("Coach: Cadê o vídeo, filhão? Digita o bagulho direito: /video nome_do_arquivo.mp4")
                continue
                
            caminho_video = partes[1].strip()
            
            try:
                # Manda pro nosso handler fazer o upload e esperar
                arquivo_video = processar_vod(caminho_video)
                
                # A instrução secreta que a gente manda junto com o vídeo pro Coach
                prompt_analise = "Analise esse VOD de Valorant. Me aponte os erros de posicionamento, mira, uso de skill e tomada de decisão. Coloque os tempos exatos do vídeo (timestamps). Seja o Coach Frttt e não perdoe as pinadas."
                
                # O PULO DO GATO: Mandando os dois juntos numa lista [ ]
                response = chat.send_message([arquivo_video, prompt_analise])
                
                # Salvando no banco (salvamos só um aviso pra não bugar o texto do SQLite)
                salvar_mensagem("user", f"[Enviou o VOD para análise: {caminho_video}]")
                salvar_mensagem("model", response.text)
                
                print(f"\nCoach:\n{response.text}\n")
                
            except Exception as e:
                print(f"\n[Sistema] Deu zica na hora de ler o vídeo, truta. Olha o erro: {e}")
                
        # 2. FLUXO NORMAL DE TEXTO
        else:
            salvar_mensagem("user", mensagem)
            response = chat.send_message(mensagem)
            salvar_mensagem("model", response.text)
            print(f"\nCoach:\n{response.text}\n")

if __name__ == "__main__":
    main()