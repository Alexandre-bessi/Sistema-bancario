import re

# Lista para armazenar usuários
usuarios = []
# Lista para armazenar contas
contas = []

# Função para validar a data de nascimento no formato DD/MM/AAAA
def validar_data(data):
    return re.match(r"^\d{2}/\d{2}/\d{4}$", data)

# Função para validar o CPF no formato numérico com 11 dígitos
def validar_cpf(cpf):
    return re.match(r"^\d{11}$", cpf)

# Função para criar um usuário
def criar_usuario(nome, data_nascimento, cpf, endereco, is_admin=False):
    # Verifica se o CPF já está cadastrado
    if cpf in [u["cpf"] for u in usuarios]:
        print("CPF já cadastrado!")
        return False
    # Verifica se a data de nascimento está no formato correto
    if not validar_data(data_nascimento):
        print("Data de nascimento inválida! Use o formato DD/MM/AAAA.")
        return False
    # Verifica se o CPF está no formato correto
    if not validar_cpf(cpf):
        print("CPF inválido! Use apenas números (11 dígitos).")
        return False
    # Adiciona o usuário à lista de usuários
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco, "is_admin": is_admin})
    print(f"Usuário '{nome}' criado com sucesso!")
    return True

# Função para criar uma conta corrente
def criar_conta_corrente(usuario):
    # Número da conta é determinado pelo tamanho da lista de contas
    numero_conta = len(contas) + 1
    # Usuário define o limite de saque inicial
    limite = float(input("Informe o limite de saque inicial: "))
    # Adiciona a conta à lista de contas
    contas.append({"agencia": "000", "numero_conta": numero_conta, "usuario": usuario, "saldo": 0, "extrato": "", "limite": limite, "numero_saques": 0})
    print(f"Conta corrente criada com sucesso! Número da conta: {numero_conta}")

# Função para apagar um usuário, apenas se o usuário atual for administrador
def apagar_usuario(cpf, usuario_atual):
    if not usuario_atual.get("is_admin"):
        print("Apenas o administrador pode excluir perfis!")
        return
    # Filtra a lista de usuários e contas, removendo o usuário com o CPF fornecido
    global usuarios, contas
    usuarios = [u for u in usuarios if u["cpf"] != cpf]
    contas = [c for c in contas if c["usuario"]["cpf"] != cpf]
    print(f"Usuário com CPF {cpf} excluído com sucesso!")

# Função para realizar um depósito
def depositar(usuario, valor):
    for c in contas:
        if c["usuario"] == usuario:
            # Atualiza o saldo e registra o depósito no extrato
            c["saldo"] += valor
            c["extrato"] += f"Depósito: R$ {valor:.2f}\n"
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
            return
    print("Conta não encontrada!")

# Função para realizar um saque
def sacar(usuario, *, valor):
    for c in contas:
        if c["usuario"] == usuario:
            # Verifica se o saldo, limite e número de saques permitem a operação
            if valor > c["saldo"]:
                print("Operação falhou! Você não tem saldo suficiente.")
            elif valor > c["limite"]:
                print("Operação falhou! O valor do saque excede o limite.")
            elif c["numero_saques"] >= 3:
                print("Operação falhou! Número máximo de saques excedido.")
            else:
                # Atualiza o saldo, registra o saque no extrato e incrementa o número de saques
                c["saldo"] -= valor
                c["extrato"] += f"Saque: R$ {valor:.2f}\n"
                c["numero_saques"] += 1
                print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
            return
    print("Conta não encontrada!")

# Função para alterar o limite de saque baseado em uma porcentagem do saldo total
def alterar_limite(usuario, percentual):
    for c in contas:
        if c["usuario"] == usuario:
            # Calcula o novo limite com base no saldo e percentual fornecidos
            novo_limite = c["saldo"] * (percentual / 100)
            c["limite"] = novo_limite
            print(f"Novo limite de saque: R$ {novo_limite:.2f}")
            return
    print("Conta não encontrada!")

# Função para exibir o extrato e/ou saldo atual
def extrato(usuario, saldo_atual=False, extrato_atual=False):
    for c in contas:
        if c["usuario"] == usuario:
            if saldo_atual:
                print(f"Saldo: R$ {c['saldo']:.2f}")
            if extrato_atual:
                print("\n================ EXTRATO ================")
                print("Não foram realizadas movimentações." if not c["extrato"] else c["extrato"])
                print("==========================================")
            return
    print("Conta não encontrada!")

# Menu principal para interação com o usuário
menu_principal = """
================ MENU ===============
[c] Criar usuário
[l] Login
[f] Excluir usuário
[q] Sair
==========================================
=> """

# Menu de operações do usuário
menu_usuario = """
================ MENU ===============
[d] Depositar
[s] Sacar
[e] Extrato
[a] Alterar limite de saque
[q] Sair
==========================================
=> """

# Criação do primeiro usuário como administrador
while not usuarios:
    print("Criação do primeiro usuário (administrador):")
    nome_admin = input("Informe o nome do administrador: ")
    data_nascimento_admin = input("Informe a data de nascimento do administrador: ")
    cpf_admin = input("Informe o CPF do administrador: ")
    endereco_admin = input("Informe o endereço do administrador (logradouro - numero - bairro - cidade/sigla do estado): ")
    if criar_usuario(nome_admin, data_nascimento_admin, cpf_admin, endereco_admin, is_admin=True):
        print("Administrador criado com sucesso!")

# Loop principal para interação com o sistema
while True:
    opcao = input(menu_principal)

    if opcao == "c":
        nome_usuario = input("Informe o nome do usuário: ")
        data_nascimento = input("Informe a data de nascimento do usuário: ")
        cpf = input("Informe o CPF do usuário: ")
        endereco = input("Informe o endereço do usuário (logradouro - numero - bairro - cidade/sigla do estado): ")
        criar_usuario(nome_usuario, data_nascimento, cpf, endereco)

    elif opcao == "l":
        cpf_usuario = input("Informe o CPF do usuário: ")
        usuario_atual = next((u for u in usuarios if u["cpf"] == cpf_usuario), None)
        if usuario_atual:
            criar_conta_corrente(usuario_atual)
            while True:
                opcao_usuario = input(menu_usuario)

                if opcao_usuario == "d":
                    valor = float(input("Informe o valor do depósito: "))
                    depositar(usuario_atual, valor)

                elif opcao_usuario == "s":
                    valor = float(input("Informe o valor do saque: "))
                    sacar(usuario_atual, valor=valor)

                elif opcao_usuario == "e":
                    extrato(usuario_atual, saldo_atual=True, extrato_atual=True)

                elif opcao_usuario == "a":
                    percentual = float(input("Informe a porcentagem do saldo para definir o novo limite de saque: "))
                    alterar_limite(usuario_atual, percentual)

                elif opcao_usuario == "q":
                    break

                else:
                    print("Operação inválida, por favor selecione novamente a operação desejada.")
        else:
            print("Usuário não encontrado!")

    elif opcao == "f":
        cpf_usuario = input("Informe o CPF do usuário a ser excluído: ")
        apagar_usuario(cpf_usuario, usuario_atual)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
