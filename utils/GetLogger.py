import logging
from colorama import Fore, Style
from dotenv import load_dotenv
import os


def create_logger() -> logging.Logger:
    """
    Cria e configura um logger personalizado com cores para diferentes níveis de log.

    O logger é configurado para exibir mensagens no console (stdout) com cores
    diferentes para cada nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    O nível de log é definido pela variável de ambiente 'LOGGING_LEVEL'.

    Returns:
        logging.Logger: Um objeto logger configurado.
    """
    load_dotenv()
    nivel_de_log = int(os.environ.get("LOGGING_LEVEL", "1")) # Default to INFO if not set
    niveis_de_log = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
    nivel_de_log_selecionado = niveis_de_log[nivel_de_log]

    
    class FormatadorColorido(logging.Formatter):
        """
        Um formatador de log personalizado que adiciona cores às mensagens de log
        baseado no nível de log.
        """
        def format(self, registro):
            """
            Formata o registro de log, adicionando cores à mensagem.

            Args:
                registro (logging.LogRecord): O registro de log a ser formatado.

            Returns:
                str: A mensagem de log formatada com cores.
            """
            mapa_de_cores = {
                logging.DEBUG: Fore.BLUE,
                logging.INFO: Fore.GREEN,
                logging.WARNING: Fore.YELLOW,
                logging.ERROR: Fore.RED,
                logging.CRITICAL: Fore.RED + Style.BRIGHT,
            }
            registro.msg = mapa_de_cores.get(registro.levelno, Fore.WHITE) + str(registro.msg) + Style.RESET_ALL
            return super().format(registro)

    # Configura o logger
    logger = logging.getLogger(__name__)
    logger.setLevel(nivel_de_log_selecionado)

    manipulador_de_stream = logging.StreamHandler()
    manipulador_de_stream.setFormatter(FormatadorColorido('%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s'))

    logger.addHandler(manipulador_de_stream)
    return logger


logger = create_logger()