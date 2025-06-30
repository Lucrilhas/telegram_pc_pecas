import re
import unicodedata

def clean_text(text: str) -> str:
    """
    Limpa um texto removendo acentos, espaços múltiplos, pontuações específicas e normalizando underscores.

    Args:
        text (str): O texto a ser limpo.

    Returns:
        str: O texto limpo.

    """
    text = ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')

    text = re.sub(r'\s+', '_', text).strip()

    text = re.sub(r'_+', '_', text)

    pontuacao_remover = r"[,;.\\/]"
    text = re.sub(pontuacao_remover, '', text)

    return text