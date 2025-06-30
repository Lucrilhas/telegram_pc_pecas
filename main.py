import telebot
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from utils.GetLogger import logger
from data.DadosGeraisDS import DadosGerais
from utils.Iniciar import inicializar


# --- 1. CONFIGURAÇÃO INICIAL ---
client, bot, id_chat_usuario = inicializar()

# --- 2. LÓGICA DE MONITORAMENTO ---

# Este decorador do Telethon diz: "quando uma nova mensagem chegar..."
@client.on(events.NewMessage(chats=DadosGerais.canais_alvo))
async def handler_nova_mensagem(event):
    """
    Esta função é chamada automaticamente pela Telethon sempre que uma
    nova mensagem é postada em um dos 'canais_alvo'.
    """
    mensagem = event.message
    # Garante que temos o username para criar o link
    if not hasattr(event.chat, 'username') or not event.chat.username:
        logger.warning(f"Mensagem recebida de um canal sem username. Não é possível criar link.")
        return

    canal_username = event.chat.username
    
    # Pega o texto da mensagem. Pode estar em .text ou em .caption (para mídias)
    texto_da_mensagem = (mensagem.text or mensagem.caption or "").lower()

    logger.debug(f"Nova mensagem recebida de @{canal_username}. Verificando...")

    # Se não houver texto, não há o que fazer
    if not texto_da_mensagem:
        return

    # Procura cada palavra-chave no texto da mensagem
    achou = False
    for palavra in DadosGerais.palavras_chave:
        if palavra.lower() in texto_da_mensagem:
            logger.info(f"🚨 **ALERTA!** 🚨 -> 🔎 Palavra-chave encontrada: `{palavra}` -- 📢 Canal: `@{canal_username}`")
            achou = True
            
            # --- Início: Lógica de envio da notificação ---

            # 1. Cria o link direto para a mensagem original
            link_mensagem = f"https://t.me/{canal_username}/{mensagem.id}"
            
            # 2. Monta o texto da notificação
            texto_notificacao = (
                f"✅ *Encontrou a palavra chave!*\n\n"
                f"🔑 *Palavra:* `{palavra}`\n"
                f"📢 *Canal:* @{canal_username}\n\n"
                f"🔗 [Clique aqui para ver a mensagem]({link_mensagem})"
            )

            # 3. Envia a mensagem para o seu chat pessoal usando o bot
            try:
                bot.send_message(id_chat_usuario, texto_notificacao, parse_mode='Markdown')
                logger.info(f"Notificação enviada com sucesso para o seu Telegram.")
            except Exception as e:
                logger.error(f"Falha ao enviar notificação para o Telegram: {e}")

            # --- Fim: Lógica de envio da notificação ---
            break

    if not achou:
        # Apenas loga no console, não envia mensagem no Telegram para evitar spam.
        # Veja a explicação abaixo.
        logger.debug(f"Nenhuma palavra-chave encontrada em @{canal_username}. Mensagem: {texto_da_mensagem.replace('\n', ' ')}\n")


# --- 3. EXECUÇÃO ---
async def main():
    logger.info("Iniciando o bot de notificações...")
    # Teste inicial para garantir que o bot consegue enviar mensagem
    bot.send_message(id_chat_usuario, "🤖 Bot de monitoramento iniciado e pronto para enviar alertas!")

    logger.info("Iniciando o cliente para monitorar os canais...")
    await client.start()
    logger.info("Cliente conectado e monitorando ativamente os canais!")
    await client.run_until_disconnected()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())