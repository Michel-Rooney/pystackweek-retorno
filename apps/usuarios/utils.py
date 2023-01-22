from django.contrib import messages

def cadastro_is_valid(request, nome: str, email: str, senha: str, confirmar_senha: str):
    if (len(nome.strip()) == 0) or (len(email.strip()) == 0) or (len(senha.strip()) == 0) or (len(confirmar_senha.strip()) == 0):
        messages.error(request, 'Preencha todos os campos')
        return False
    if senha != confirmar_senha:
        messages.error(request, 'As senhas não coicidem')
        return False
    return True 