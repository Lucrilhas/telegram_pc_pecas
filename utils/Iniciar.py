from telethon import TelegramClient
from os import getenv
from dotenv import load_dotenv
import telebot

def inicializar():
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Credenciais para o Cliente (sua conta de usuário)
    api_id = int(getenv("API_ID"))
    api_hash = getenv("API_HASH")

    # Credenciais para o Bot (que vai te notificar)
    tele_token = getenv("TELEGRAM_TOKEN")
    id_chat_usuario = int(getenv("CHAT_ID"))

    # Validação das variáveis
    if not all([api_id, api_hash, tele_token, id_chat_usuario]):
        raise ValueError("Uma ou mais variáveis de ambiente não foram definidas. Verifique seu arquivo .env")

    # Cria uma sessão para o Telethon para não precisar logar toda vez
    client = TelegramClient('anon', api_id, api_hash)

    # Inicializa o bot que vai enviar as notificações para você
    bot = telebot.TeleBot(tele_token)

    return client, bot, id_chat_usuario