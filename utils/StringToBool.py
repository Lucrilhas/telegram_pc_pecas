def string_to_bool(s: str) -> bool:
    """
    Converte uma string para um valor booleano.

    A string de entrada é convertida para minúsculas e espaços em branco
    no início e no final são removidos antes da conversão.

    Args:
        s: A string a ser convertida.

    Returns:
        True se a string for "true" ou "1" (ignorando maiúsculas/minúsculas).
        False se a string for "false" ou "0" (ignorando maiúsculas/minúsculas).

    Raises:
        ValueError: Se a string não for "true", "false", "1" ou "0" (ignorando maiúsculas/minúsculas).
    """
    s = s.strip().lower()

    if s == "true" or s == "1":
        return True
    elif s == "false" or s == "0":
        return False
    else:
        raise ValueError(f"String booleana inválida: '{s}'")