def verificar_senha(senha):
    import conexao
    # Verifica se a senha fornecida corresponde ao hash armazenado no banco de dados
    try:
        conexao.cursor.execute("SELECT hash FROM senha_mestre ORDER BY id DESC LIMIT 1")
        resultado = conexao.cursor.fetchone()
        if resultado is None:
            print("Nenhuma senha mestre encontrada no banco de dados.")
            return False

        hash_armazenado = resultado[0]
        import bcrypt
        # Verifica se a senha fornecida corresponde ao hash armazenado
        if bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado):
            print("Senha mestre verificada com sucesso!")
            return True
        else:
            print("Senha mestre incorreta.")
            return False
    except Exception as e:
        print(f"Erro ao verificar senha: {e}")
        return False