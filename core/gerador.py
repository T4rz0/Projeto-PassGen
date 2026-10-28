
#Função para gerar senha com numeros e caracteres 
def gerar_senha(comprimento, incluir_numeros, incluir_caracteres_especiais):
    #Faz a senha ser randomica
    import random
    #traz a possibilidade de usar letras na senha
    import string

    #coloca dentro da variavel caracteres todas as letras do alfabeto
    caracteres = string.ascii_letters

    #Se quiser adicionar numeros adiciona
    if incluir_numeros == True:
        caracteres += string.digits

    #Se quiser caracter especial tipo !@%* adiciona
    if incluir_caracteres_especiais == True:
        caracteres += string.punctuation

    #Junta tudo e randomiza gerando uma senha
    senha = ''.join(random.choice(caracteres) for _ in range(comprimento))
    return senha
