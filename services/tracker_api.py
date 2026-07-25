import requests
import urllib.parse

def buscar_dados_tracker(riot_id_input):
    """
    Busca os dados reais do jogador usando os endpoints mais estáveis da API pública do HenrikDev.
    """
    limpo = riot_id_input.strip()
    
    if "#" in limpo:
        name, tag = limpo.split("#", 1)
    else:
        name, tag = limpo, "BR1"

    name_encoded = urllib.parse.quote(name)
    headers = {"User-Agent": "CoachFrtttBot/3.0"}
    
    dados_texto = f"Perfil consultado para: {name}#{tag}\n"
    
    try:
        # 1. Puxa dados gerais da conta (Nível e Região)
        url_account = f"https://api.henrikdev.xyz/v1/account/{name_encoded}/{tag}"
        resp_acc = requests.get(url_account, headers=headers, timeout=8)
        
        if resp_acc.status_code == 200:
            acc_json = resp_acc.json()
            if acc_json.get("status") == 200:
                acc_data = acc_json.get("data", {})
                dados_texto += f"- Conta Nível: {acc_data.get('account_level', 'Desconhecido')}\n"
                dados_texto += f"- Região: {acc_data.get('region', 'br').upper()}\n"

        # 2. Puxa o MMR/Elo usando a rota v1 (mais atualizada e estável)
        url_mmr = f"https://api.henrikdev.xyz/v1/mmr/br/{name_encoded}/{tag}"
        resp_mmr = requests.get(url_mmr, headers=headers, timeout=8)
        
        if resp_mmr.status_code == 200:
            mmr_json = resp_mmr.json()
            if mmr_json.get("status") == 200:
                mmr_data = mmr_json.get("data", {})
                currenttier = mmr_data.get("currenttierpatched", "Não ranqueado")
                ranking_in_tier = mmr_data.get("ranking_in_tier", 0)
                
                dados_texto += f"- Elo Atual: {currenttier} ({ranking_in_tier} RR)\n"
            else:
                dados_texto += "- Elo: Conta sem ranqueada recente na região BR.\n"
        else:
            dados_texto += "- Elo: Indisponível temporariamente na API.\n"
            
        return dados_texto
        
    except Exception as e:
        return f"Erro ao conectar na API do Valorant: {e}"