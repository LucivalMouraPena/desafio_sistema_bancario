import textwrap
from colorama import Fore, Style, init

# Inicializa o Colorama (para cores no terminal)
init(autoreset=True)

# Função para exibir o menu principal e capturar a opção do usuário
def exibir_menu():
    menu = f"""\n
{Fore.CYAN}============= MENU PRINCIPAL =============
[d] Depositar
[s] Sacar
[e] Extrato
[cu] Criar Usuário
[cc] Criar Conta
[lc] Listar Contas
[q] Sair
=> {Style.RESET_ALL}"""
    return input(textwrap.dedent(menu))

# Função para realizar um depósito
def realizar_deposito(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"{Fore.GREEN}Depósito:\tR$ {valor:.2f}\n"
        print(f"{Fore.GREEN}✔ Depósito realizado com sucesso!")
    else:
        print(f"{Fore.RED}✘ Valor inválido para depósito!")
    return saldo, extrato

# Função para realizar um saque
def realizar_saque(*, saldo, valor, extrato, limite, saques_hoje, max_saques):
    if valor > saldo:
        print(f"{Fore.RED}✘ Saldo insuficiente.")
    elif valor > limite:
        print(f"{Fore.RED}✘ Valor excede o limite permitido.")
    elif saques_hoje >= max_saques:
        print(f"{Fore.RED}✘ Número máximo de saques atingido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"{Fore.RED}Saque:\t\tR$ {valor:.2f}\n"
        saques_hoje += 1
        print(f"{Fore.GREEN}✔ Saque realizado com sucesso!")
    else:
        print(f"{Fore.RED}✘ Valor inválido para saque.")
    return saldo, extrato, saques_hoje

# Função para mostrar o extrato
def mostrar_extrato(saldo, /, *, extrato):
    print(f"\n{Fore.YELLOW}========== EXTRATO ==========")
    print(extrato if extrato else "Sem movimentações.")
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("=" * 30)

# Cria um novo usuário
def cadastrar_usuario(lista_usuarios):
    cpf = input("Informe o CPF (apenas números): ")
    if buscar_usuario(cpf, lista_usuarios):
        print(f"{Fore.RED}✘ Usuário já existe com este CPF.")
        return

    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço (rua, nº - bairro - cidade/UF): ")

    lista_usuarios.append({
        "nome": nome,
        "data_nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    print(f"{Fore.GREEN}✔ Usuário cadastrado com sucesso!")

# Verifica se o usuário existe
def buscar_usuario(cpf, lista_usuarios):
    return next((user for user in lista_usuarios if user["cpf"] == cpf), None)

# Cria uma conta para um usuário já existente
def cadastrar_conta(agencia, numero_conta, lista_usuarios):
    cpf = input("Informe o CPF do titular: ")
    usuario = buscar_usuario(cpf, lista_usuarios)

    if usuario:
        print(f"{Fore.GREEN}✔ Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print(f"{Fore.RED}✘ CPF não encontrado. Conta não criada.")

# Lista todas as contas cadastradas
def listar_todas_contas(lista_contas):
    for conta in lista_contas:
        print("=" * 50)
        print(f"Agência: {conta['agencia']}")
        print(f"Número da Conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print("=" * 50)

# Função principal
def main():
    AGENCIA = "0001"
    LIMITE_SAQUE = 3

    saldo = 0
    limite = 500
    extrato = ""
    saques_hoje = 0
    usuarios = []
    contas = []

    while True:
        opcao = exibir_menu()

        if opcao == "d":
            valor = float(input("Valor para depósito: "))
            saldo, extrato = realizar_deposito(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Valor para saque: "))
            saldo, extrato, saques_hoje = realizar_saque(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                saques_hoje=saques_hoje,
                max_saques=LIMITE_SAQUE
            )

        elif opcao == "e":
            mostrar_extrato(saldo, extrato=extrato)

        elif opcao == "cu":
            cadastrar_usuario(usuarios)

        elif opcao == "cc":
            numero_conta = len(contas) + 1
            nova_conta = cadastrar_conta(AGENCIA, numero_conta, usuarios)
            if nova_conta:
                contas.append(nova_conta)

        elif opcao == "lc":
            listar_todas_contas(contas)

        elif opcao == "q":
            print(f"{Fore.CYAN}Obrigado por usar nosso sistema! Até logo.")
            break

        else:
            print(f"{Fore.RED}✘ Opção inválida. Tente novamente.")

# Executa o programa
main()
