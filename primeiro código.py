usuarios = {}

menu_principal = """
================ MENU ===============
[c] Criar usuário
[l] Login
[q] Sair
==========================================
=> """

menu_usuario = """
================ MENU ===============
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
==========================================
=> """

while True:
    opcao = input(menu_principal)

    if opcao == "c":
        nome_usuario = input("Informe o nome do usuário: ")
        usuarios[nome_usuario] = {"saldo": 0, "limite": 500, "extrato": "", "numero_saques": 0}
        print(f"Usuário '{nome_usuario}' criado com sucesso!")

    elif opcao == "l":
        nome_usuario = input("Informe o nome do usuário: ")
        if nome_usuario in usuarios:
            usuario_atual = usuarios[nome_usuario]
            while True:
                opcao_usuario = input(menu_usuario)

                if opcao_usuario == "d":
                    valor = float(input("Informe o valor do depósito: "))
                    if valor > 0:
                        usuario_atual["saldo"] += valor
                        usuario_atual["extrato"] += f"Depósito: R$ {valor:.2f}\n"
                    else:
                        print("Operação falhou! O valor informado é inválido.")

                elif opcao_usuario == "s":
                    valor = float(input("Informe o valor do saque: "))
                    excedeu_saldo = valor > usuario_atual["saldo"]
                    excedeu_limite = valor > usuario_atual["limite"]
                    excedeu_saques = usuario_atual["numero_saques"] >= 3

                    if excedeu_saldo:
                        print("Operação falhou! Você não tem saldo suficiente.")
                    elif excedeu_limite:
                        print("Operação falhou! O valor do saque excede o limite.")
                    elif excedeu_saques:
                        print("Operação falhou! Número máximo de saques excedido.")
                    elif valor > 0:
                        usuario_atual["saldo"] -= valor
                        usuario_atual["extrato"] += f"Saque: R$ {valor:.2f}\n"
                        usuario_atual["numero_saques"] += 1
                    else:
                        print("Operação falhou! O valor informado é inválido.")

                elif opcao_usuario == "e":
                    print("\n================ EXTRATO ================")
                    print("Não foram realizadas movimentações." if not usuario_atual["extrato"] else usuario_atual["extrato"])
                    print(f"\nSaldo: R$ {usuario_atual['saldo']:.2f}")
                    print("==========================================")

                elif opcao_usuario == "q":
                    break

                else:
                    print("Operação inválida, por favor selecione novamente a operação desejada.")

        else:
            print("Usuário não encontrado!")

    elif opcao == "q":
        break
