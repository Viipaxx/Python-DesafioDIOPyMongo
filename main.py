import pprint


class Cliente:

    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf
        self.enderecos = []
        self.contas = []

    def adicionar_conta(self, tipo, agencia, numero, id_cliente, saldo=0):
        self.contas.append(Conta(tipo, agencia, numero, id_cliente, saldo))
        print('\n=== Conta adicionada com sucesso. ===')

    def get_contas(self):
        if len(self.contas) == 0:
            return '\nNenhuma conta adicionada.'
        else:
            contas = ''
            for conta in self.contas:
                contas += f'{conta}\n'
            return contas

    def adicionar_endereco(self, logradouro, numero, complemento,  bairro, cep, sguf):

        endereco = f'{logradouro}, nº {numero} {complemento} - {bairro}, {cep}, {sguf}'
        self.enderecos.append(endereco)
        print('\n=== Endereço adicionado com sucesso. ===')

    def get_enderecos(self):
        return self.enderecos
        pass  # FIXME: Vai retornar a lista de endereços do cliente informado

    def listar_enderecos(self, cpf):
        for endereco in self.enderecos:
            print(endereco)
        pass  # FIXME: Vai listar os endereços do cliente informado

    def __str__(self):
        return self.nome

class Conta:

    def __init__(self, tipo, agencia, numero, cpf, saldo):
        self.id = 1
        self.tipo = tipo
        self.agencia = agencia
        self.numero = numero
        self.cpf = cpf
        self.saldo = saldo

    def associar_conta(self, cpf):

        pass

    def __str__(self):
        return f'\n================================' \
               f'\nID: {self.id}' \
               f'\nTipo: {self.tipo}' \
               f'\nAgência: {self.agencia}' \
               f'\nNúmero: {self.numero}' \
               f'\nProprietário: {self.id_cliente}' \
               f'\nSaldo: R$ {self.saldo:.2f}'


c1 = Cliente('Vitor', '71415415439')
c1.adicionar_conta('CC', '0001', '1001', c1.cpf, 100)

print(c1.get_contas())