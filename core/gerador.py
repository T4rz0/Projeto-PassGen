#Função para gerar senha com numeros e caracteres 
def gerar_senha(comprimento, incluir_numeros, incluir_caracteres_especiais):
    #faz a senha ser randomica
    import random
    #traz a possibilidade de usar letras
    import string

    #coloca dentro da variavel caracteres todas as letras do alfabeto
    caracteres = string.ascii_letters  # Letras maiúsculas e minúsculas

    if incluir_numeros:
        caracteres += string.digits  # Adiciona números

    if incluir_caracteres_especiais:
        caracteres += string.punctuation  # Adiciona caracteres especiais

    senha = ''.join(random.choice(caracteres) for _ in range(comprimento))
    return senha