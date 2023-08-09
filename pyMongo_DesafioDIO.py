import pprint
from datetime import datetime
from random import randint
from textwrap import dedent
from pymongo import MongoClient


class Banco:

    servidor = None
    def connection(self):
        try:
            print("\n=== Banco conectado ===")
            self.servidor = MongoClient(f'mongodb+srv://root:root1227@serverspeed.cqdjurk.mongodb.net/?retryWrites=true&w=majority')
            return self.servidor

        except:
            print('\n@@@ Conexão falhou. @@@')

    def desconnection(self):
        self.servidor.close()
        print("\n=== Banco desconectado ===")


class Cliente:

    def __init__(self, nome, cpf):
        nome = nome.split()
        self.full_name = ' '.join(nome)
        self.first_name = nome[0]
        self.last_name = nome[-1]
        self.cpf = cpf
        self.enderecos = []
        self.contas = []

    def adicionar_endereco(self, logradouro, numero, bairro, cep, sguf):
        endereco = f'{logradouro}, nº{numero} - {bairro}, {cep}, {sguf}'
        self.enderecos.append(endereco)
        print('\n=== Endereço adicionado com sucesso. ===')

    def listar_enderecos(self):
        enderecos = '\t\tEndereços:'

        for endereco in self.enderecos:
            enderecos += f'\n{endereco}'

        return enderecos

    def adicionar_conta(self):
        tipo = ''
        agencia = ''
        numero = ''
        id_cliente = ''
        saldo = 0

        self.contas.append(Conta(tipo, agencia, numero, id_cliente, saldo=0))

        return  '\n=== Conta adicionada com sucesso. ==='

    def listar_contas(self):
        contas = '\t\tContas'

        for conta in self.contas:
            contas += f'\n{conta}'

        return contas


class Conta:

    def __init__(self, tipo, agencia, numero, id_cliente, saldo):
        self.id = ''
        self.tipo = tipo
        self.agencia = agencia
        self.numero = numero
        self.id_cliente = id_cliente
        self.saldo = saldo


def verificar_conta(contas, user, numero):

    conta = contas.find_one({"número": numero})

    if not conta:
        print("\n@@@ Conta não encotrada. @@@")
        return False
    else:
        if conta["id_cliente"] == user["_id"]:
            return True
        else:
            print('\n@@@ Conta inválida. @@@')
            return False


def validar_numero_conta(contas , numero_conta):
    verificao_numero = contas.find_one({"número": numero_conta})

    while verificao_numero != None:
        numero_conta = randint(10000, 999999)
        verificao_numero = contas.find_one({"número": numero_conta})

    return numero_conta


def validar_cpf(users, cpf):

    validacao = users.find_one({"cpf": cpf})

    if validacao is None:
        return True
    else:
        return False


def registrar(users):

    cpf = input("Digite seu CPF (sem pontuação): ")

    if len(cpf) < 11:
        print('\n@@@ Operação interrompida. CPF inválido. @@@')
        return False

    if validar_cpf(users, cpf):
        nome = input("Digite seu nome completo: ")
        password = input("Digite sua senha: ")
        confirm_password = input("Confirme sua senha: ")

        if password == confirm_password:
            users.insert_one({
                "nome": nome,
                "cpf": cpf,
                "password": password,
                "endereços": [],
                "contas": []
            })
            print("\n=== Conta criada com sucesso ===")
            return True
        else:
            print("\n@@@ Operação interrompida. Cadastro mal sucedido. @@@")
            return False
    else:
        print('\n@@@ Operação interrompida. Usuário já cadastrado. @@@')
        return False


def associar_conta(conta, users, user):

    user["contas"].append(conta["_id"])

    query = {"_id": user["_id"]}
    newValue = {"$set": user}

    users.update_one(query, newValue)


def abrir_conta(contas, users, id_user):

    conta = {
        "tipo": "cc",
        "agência": "0001",
        "número": validar_numero_conta(contas, randint(10000, 999999)),
        "id_cliente": id_user["_id"],
        "saldo": 0,
        "created_at": (datetime.now().strftime("%d/%m/%Y %H:%M")),
    }

    contas.insert_one(conta)

    conta_criada = contas.find_one({"número": conta["número"]}, {"saldo": 0})

    print('\n=== Conta criada com sucesso ===')
    print('\nDados da conta:\n')
    for c, k in conta_criada.items():
        print(f"{c}: {k}")

    associar_conta(conta_criada, users, id_user)


def get_user_by_cpf(users, cpf):
    return users.find_one({"cpf": cpf})


def get_user_by_id(users, id):
    return users.find_one({"_id": id})


def get_conta_by_numero(contas, num_conta):
    return contas.find_one({"número": num_conta})



def get_conta_by_id(contas, id):
    return contas.find_one({"_id": id})


def login(users):
    cpf = input("Digite seu CPF (sem pontuação): ")

    if len(cpf) < 11:
        print('\n@@@ Operação interrompida. CPF inválido. @@@')
        return False, None

    if validar_cpf(users, cpf):
        print('\n@@@ Operação interrompida. Conta não registrada. @@@')
        return False, None
    else:
        id_user = get_user_by_cpf(users, cpf)
        password = input("Sua senha: ")

        if password == id_user["password"]:
            print("\n=== Logado com sucesso ===")
            return True, id_user
        else:
            print("\n@@@ Operação interrompida. Senha incorreta @@@")
            return False, None


def menu_principal():
    return """
[c] - Conectar-se
[r] - Registrar-se
[q] - Sair
-> """


def menu_usuario():
    return """
[ec] - Entrar na Conta
[ac] - Abrir Conta
[fc] - Fechar Conta
[lc] - Listar Contas
[q] - Voltar
-> """


def menu_conta():
    return """
[d] - Depóstio
[s] - Saque
[e] - Empréstimo
[cs] = Consultar Saldo
[rt] - Realizar Transferência
[sc] - Solicitar Cartão
[q] - Voltar
-> """


def verificar_valor(valor):
    if valor <= 0:
        return False
    else:
        return True

def deposito(contas, num_conta, valor):

    if not verificar_valor(valor):
        print('\n@@@ Operação interrompida. Valor inválido. @@@')
        return False

    else:
        conta = get_conta_by_numero(contas, num_conta)
        saldo_antigo = conta["saldo"]
        saldo_atual = (saldo_antigo + valor) * 1.0

        my_query = {"número": num_conta}
        new_values = {"$set": {"saldo": saldo_atual}}

        contas.update_one(my_query, new_values)
        print('\n=== Depósito realizado com sucesso. ===')
        return True


def saque(contas, num_conta, valor):
    if not verificar_valor(valor):
        print('\n@@@ Operação interrompida. Valor inválido. @@@')
        return False

    else:
        conta = get_conta_by_numero(contas, num_conta)
        saldo_antigo = conta["saldo"]

        if valor > saldo_antigo:
            print('\n@@@ Operação interrompida. Saldo insuficiente. @@@')
            return False

        else:
            saldo_atual = saldo_antigo - valor

            my_query = {"número": num_conta}
            new_values = {"$set": {"saldo": saldo_atual}}

            contas.update_one(my_query, new_values)
            print('\n=== Saque realizado com sucesso. ===')
            return True


def transferencia(contas, users, num_conta_remetente, num_conta_destino, valor):
    if not verificar_valor(valor):
        print('valor inválido')
    else:
        conta_destino = get_conta_by_numero(contas, num_conta_destino)

        if conta_destino is None:
            print('Conta não existente')

        else:
            user_destino = get_user_by_id(users, conta_destino["id_cliente"])
            print(user_destino)
            print(f'Transferência para {user_destino["nome"].title()}')


def listar_contas(contas, user):
    for number, id_conta in enumerate(user["contas"]):
        conta = get_conta_by_id(contas, id_conta)
        print(f'\n=== Conta {number + 1} ===\n')
        for k, v in conta.items():
            print(f"{k}: {v}")


def consultar_saldo(contas, num_conta):
    conta = get_conta_by_numero(contas, num_conta)

    print(f"\nSaldo: R$ {conta['saldo']:.2f}")


while True:

    conexao = Banco()
    client = conexao.connection()
    db = client["DIO-Bank"]
    users = db.users
    contas = db.contas

    opcao = dedent(input(menu_principal()))

    if opcao == 'c':

        result, user = login(users)
        if result:
            while True:
                opcao = dedent(input(menu_usuario()))

                if opcao == 'ec':
                    num_conta = int(input("Digite o número da sua conta: "))
                    conta = verificar_conta(contas, user, num_conta)

                    if conta:
                        while True:
                            opcao = dedent(input(menu_conta()))

                            if opcao == 'd':
                                valor = float(input("Digite a quantidade que deseja depositar: R$ "))
                                deposito(contas, num_conta, valor)

                            elif opcao == 's':
                                valor = float(input("Digite a quantidade que deseja sacar: R$ "))
                                saque(contas, num_conta, valor)

                            elif opcao == 'e':
                                print('empréstimo')

                            elif opcao == 'cs':
                                consultar_saldo(contas, num_conta)

                            elif opcao == 'rt':
                                print('realizar transação')

                            elif opcao == 'sc':
                                print('solicitar cartão')

                            elif opcao == 'q':
                                break

                            else:
                                print('\n@@@ Opção inválida. @@@')

                elif opcao == 'ac':
                    abrir_conta(contas, users, user)

                elif opcao == 'fc':
                    print('fechar conta')

                elif opcao == 'lc':
                    listar_contas(contas, user)

                elif opcao == 'q':
                    print('sair')
                    break

                else:
                    print('opcao invalida')

    elif opcao == 'r':

        registrar(users)

    elif opcao == 'q':
        conexao.desconnection()
        break

    else:
        print('\n@@@ Ainda não temos essa opção. @@@')
