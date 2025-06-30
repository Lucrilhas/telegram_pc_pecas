import telebot
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

# --- 1. CONFIGURAÇÃO INICIAL ---

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Credenciais para o Cliente (sua conta de usuário)
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

# Credenciais para o Bot (que vai te notificar)
tele_token = os.getenv("TELEGRAM_TOKEN")
meu_chat_id = int(os.getenv("MEU_CHAT_ID"))

# Validação das variáveis
if not all([api_id, api_hash, tele_token, meu_chat_id]):
    raise ValueError("Uma ou mais variáveis de ambiente não foram definidas. Verifique seu arquivo .env")

# Cria uma sessão para o Telethon para não precisar logar toda vez
# O arquivo 'anon.session' será criado na primeira execução
client = TelegramClient('anon', api_id, api_hash)


# --- 2. PARÂMETROS DE BUSCA ---

canais_alvo = ['@terabyteshopoficial', '@grape_tec', '@lowpricebr', '@gpcrpromo', '@guigatudo']

# Palavras-chave para procurar (em minúsculas para busca unificada)
palavras_chave = [
    "placa de vídeo", "gpu", "rtx", "geforce",
    "radeon", "rx ", "gtx", "arc a750", "arc a770",
    "4060", "4070", "4080", "4090",
    "7700 xt", "7800 xt", "7900 xtx"
]

print("Configuração carregada. Tudo pronto para começar!")


# --- 3. LÓGICA DE MONITORAMENTO (O CORAÇÃO DO SCRIPT) ---

# Este decorador do Telethon diz: "quando uma nova mensagem chegar..."
@client.on(events.NewMessage(chats=canais_alvo))
async def handler_nova_mensagem(event):
    """
    Esta função é chamada automaticamente pela Telethon sempre que uma
    nova mensagem é postada em um dos 'canais_alvo'.
    """
    mensagem = event.message
    canal_username = event.chat.username if event.chat else 'Desconhecido'
    
    # Pega o texto da mensagem. Pode estar em .text ou em .caption (para mídias)
    texto_da_mensagem = (mensagem.text or mensagem.caption or "").lower()

    print(f"Nova mensagem recebida de @{canal_username}. Verificando...")

    # Se não houver texto, não há o que fazer
    if not texto_da_mensagem:
        return

    # Procura cada palavra-chave no texto da mensagem
    achou = False
    for palavra in palavras_chave:
        if palavra in texto_da_mensagem:
            print(f"!!! PALAVRA-CHAVE ENCONTRADA: '{palavra}' em @{canal_username} !!!")

            # Formata a mensagem de alerta para enviar a você
            texto_alerta = (
                f"🚨 **ALERTA DE PROMOÇÃO!** 🚨\n\n"
                f"🔎 **Palavra-chave encontrada:** `{palavra}`\n"
                f"📢 **Canal:** `@{canal_username}`"
            )

            print(texto_alerta)


            # Para o loop assim que a primeira palavra for encontrada para não enviar múltiplos alertas da mesma mensagem
            achou = True
            break

    if not achou:
        print(f"Nenhuma palavra-chave encontrada. em {canal_username}")
            


# --- 4. EXECUÇÃO ---
async def main():

    print("Iniciando o cliente para monitorar os canais...")
    await client.start()
    print("Cliente conectado e monitorando ativamente os canais!")
    await client.run_until_disconnected()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())