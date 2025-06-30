from json import loads

def get_dict_from_text(text: str) -> dict:
    """
    Extrai um dicionário Python de uma string de texto que contém um bloco JSON delimitado por "```json" e "```".

    A função localiza o bloco JSON dentro da string, remove os delimitadores e espaços em branco extras,
    e então converte o JSON em um dicionário Python usando `json.loads()`.

    Args:
        text: A string de texto contendo o bloco JSON.

    Returns:
        Um dicionário Python representando o JSON extraído.

    Raises:
        json.JSONDecodeError: Se a string extraída não for um JSON válido.
        TypeError: Se a entrada não for uma string.
        ValueError: Se os delimitadores "```json" ou "```" não forem encontrados.

    """
    try:
        start_delimiter = "```json"
        end_delimiter = "```"

        start_index = text.find(start_delimiter)
        if start_index == -1:
            raise ValueError(f"Delimitador '{start_delimiter}' não encontrado no texto.")

        end_index = text.rfind(end_delimiter)
        if end_index == -1:
            raise ValueError(f"Delimitador '{end_delimiter}' não encontrado no texto.")

        json_text = text[start_index + len(start_delimiter):end_index].strip()
        return loads(json_text)

    except Exception as e:
        raise e