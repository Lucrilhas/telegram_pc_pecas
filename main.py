from telethon import TelegramClient, events
from utils.GetLogger import logger
from data.DadosGeraisDS import DadosGerais
from utils.Iniciar import inicializar

# --- 1. CONFIGURAÇÃO INICIAL ---
client, _, id_chat_usuario = inicializar()

# --- 2. LÓGICA DE MONITORAMENTO ---

@client.on(events.NewMessage(chats=DadosGerais.canais_alvo))
async def handler_nova_mensagem(event):
    """
    Esta função é chamada automaticamente pela Telethon sempre que uma
    nova mensagem é postada em um dos 'canais_alvo'.
    Ela agora pode lidar com múltiplas mensagens simultaneamente.
    """
    mensagem = event.message
    
    if not hasattr(event.chat, 'username') or not event.chat.username:
        logger.warning(f"Mensagem recebida de um canal sem username. Não é possível criar link.")
        return

    canal_username = event.chat.username
    texto_da_mensagem = (mensagem.text or mensagem.caption or "").lower()

    logger.debug(f"Nova mensagem recebida de @{canal_username}. Verificando...")

    if not texto_da_mensagem:
        return

    # Procura cada palavra-chave no texto da mensagem
    for palavra in DadosGerais.palavras_chave:
        if palavra.lower() in texto_da_mensagem:
            logger.info(f"🚨 **ALERTA!** 🚨 -> 🔎 Palavra-chave encontrada: `{palavra}` -- 📢 Canal: `@{canal_username}`")
            
            # --- Início: Lógica de envio da notificação (AGORA ASSÍNCRONA) ---
            
            # 1. Cria o link direto para a mensagem original
            link_mensagem = f"https://t.me/{canal_username}/{mensagem.id}"
            
            # 2. Monta o texto da notificação
            texto_notificacao = (
                f"✅ **Encontrou a palavra chave!**\n\n"
                f"🔑 **Palavra:** `{palavra}`\n"
                f"📢 **Canal:** @{canal_username}\n\n"
                f"🔗 [Clique aqui para ver a mensagem]({link_mensagem})"
            )

            # 3. Envia a mensagem para o seu chat pessoal usando o CLIENTE ASSÍNCRONO
            try:
                # A MUDANÇA CRÍTICA ESTÁ AQUI:
                # Usamos 'await client.send_message' em vez de 'bot.send_message'
                # Usamos 'parse_mode='md'' para Markdown no Telethon
                await client.send_message(id_chat_usuario, texto_notificacao, parse_mode='md')
                logger.info(f"Notificação enviada com sucesso para o seu Telegram.")
            except Exception as e:
                logger.error(f"Falha ao enviar notificação para o Telegram: {e}")

            # O 'break' aqui significa que você só envia UMA notificação,
            # mesmo que a mensagem contenha múltiplas palavras-chave. Isso geralmente é o desejado.
            break 
    # Não é mais necessário o 'if not achou', o fluxo natural do código já cobre isso.


# --- 3. EXECUÇÃO ---
async def main():
    logger.info("Iniciando o bot de notificações...")
    # Teste inicial para garantir que o bot consegue enviar mensagem
    # Também usamos o client aqui
    await client.send_message(id_chat_usuario, "🤖 Bot de monitoramento iniciado e pronto para enviar alertas!")

    logger.info("Cliente conectado e monitorando ativamente os canais!")
    # O client.start() já é chamado dentro do 'with client:' ou do client.run_until_disconnected()
    # Não precisa chamar explicitamente se usar o 'with' ou o run_until_complete(main()) no final.
    await client.run_until_disconnected()


if __name__ == '__main__':
    # A maneira recomendada de rodar o Telethon é usando-o como um context manager.
    # Ele cuida de iniciar e parar o cliente corretamente.
    print("Iniciando cliente...")
    client.start()
    print("Enviando mensagem de início...")
    # Para rodar uma corrotina fora do loop, usamos client.loop.run_until_complete
    client.loop.run_until_complete(
        client.send_message(id_chat_usuario, "🤖 Bot de monitoramento iniciado e pronto para enviar alertas!")
    )
    print("Monitorando canais... Pressione Ctrl+C para parar.")
    client.run_until_disconnected()