class gerador_senha:
    def __init__(self, comprimento, incluir_numeros, incluir_caracteres_especiais):
        self.comprimento = comprimento
        self.incluir_numeros = incluir_numeros
        self.incluir_caracteres_especiais = incluir_caracteres_especiais

#Função para gerar senha com numeros e caracteres 
def gerar_senha(comprimento, incluir_numeros, incluir_caracteres_especiais):
    #faz a senha ser randomica
    #Não é a melhor forma de gerar senhas, mas é uma forma simples e rápida
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
  # Exemplo de uso da função