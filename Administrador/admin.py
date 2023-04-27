import os
from time import sleep

import grpc
import json
import admin_pb2_grpc
import admin_pb2

def run():
    sleep_time = 0.8
    print("===================================")
    porta = input("Digite a porta para CONECTAR ao servidor: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        with grpc.insecure_channel(f'localhost:{porta}') as channel:

            stub = admin_pb2_grpc.AdminStub(channel)
            selection_string = f"\t PAINEL ADMIN\n\n1. Inserir Cliente\n2. Modificar Cliente\n3. Recuperar Cliente\n4. Apagar Cliente\n5. Inserir Produto\n6. Modificar Produto\n7. Recuperar Produto\n8. Apagar Produto\n9. Sair\n10. Adiciona cliente (Teste)\n"
            while True:
                os.system('cls')
                rpc_call = input(selection_string + "\nSelecione um serviço: ")
                if rpc_call == "1":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("========================")
                    clientId = input("Digite o ID do cliente:")
                    nome = input("Digite o nome do cliente:")
                    sobrenome = input("Digite o sobrenome do cliente:")
                    dadosCliente = {"nome": nome, "sobrenome": sobrenome}

                    request = admin_pb2.inserirClienteRequest(clientId=clientId, dadosCliente=json.dumps(dadosCliente))
                    reply = stub.inserirCliente(request)
                    print(reply.message)
                    sleep(sleep_time)
                elif rpc_call == "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("========================")
                    clientId = input("Digite o ID do cliente:")
                    nome = input("Digite o novo nome do cliente:")
                    sobrenome = input("Digite o novo sobrenome do cliente:")
                    dadosCliente = {"nome": nome, "sobrenome": sobrenome}

                    request = admin_pb2.modificarClienteRequest(clientId=clientId,
                                                                dadosCliente=json.dumps(dadosCliente))
                    reply = stub.modificarCliente(request)
                    print(reply.message)
                    sleep(sleep_time)
                elif rpc_call == "3":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("========================")
                    clientId = input("Insira o ID (cliente):")
                    request = admin_pb2.recuperarClienteRequest(clientId=clientId)
                    reply = stub.recuperarCliente(request)
                    print(reply.message)
                    sleep(sleep_time)
                elif rpc_call == "4":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("========================")
                    clientId = input("Insira o ID (cliente):")
                    request = admin_pb2.apagarClienteRequest(clientId=clientId)
                    reply = stub.apagarCliente(request)
                    print(reply.message)
                    sleep(sleep_time)
                elif rpc_call == "5":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("========================")
                    produtoId = input("Digite o ID (produto):")
                    nome = input("Digite o nome do produto:")
                    quantidade = int(input("Digite a quantidade do produto:"))
                    preco = int(input("Digite o preço do produto:"))
                    dadosProduto = {"nome": nome, "quantidade": quantidade, "preco": preco}
                    request = admin_pb2.inserirProdutoRequest(produtoId=produtoId,
                                                              dadosProduto=json.dumps(dadosProduto))
                    reply = stub.inserirProduto(request)
                    print(reply.message)
                    sleep(sleep_time)
                elif rpc_call == "6":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("========================")
                    produtoId = input("Digite o ID (produto):")
                    nome = input("Digite o nome do produto:")
                    quantidade = int(input("Digite a quantidade do produto:"))
                    preco = int(input("Digite o preço do produto:"))
                    dadosProduto = {"nome": nome, "quantidade": quantidade, "preco": preco}
                    request = admin_pb2.modificarProdutoRequest(produtoId=produtoId,
                                                                dadosProduto=json.dumps(dadosProduto))
                    reply = stub.modificarProduto(request)
                    print(reply.message)
                    sleep(sleep_time)
                elif rpc_call == "7":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("========================")
                    produtoId = input("Digite o ID (produto):")
                    request = admin_pb2.recuperarProdutoRequest(produtoId=produtoId)
                    reply = stub.recuperarProduto(request)
                    print(reply.message)
                    sleep(sleep_time)
                elif rpc_call == "8":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("========================")
                    produtoId = input("Digite o ID (produto):")
                    request = admin_pb2.apagarProdutoRequest(produtoId=produtoId)
                    reply = stub.apagarProduto(request)
                    print(reply.message)
                    sleep(sleep_time)
                elif rpc_call == "9":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Portal finalizado..")
                    sleep(sleep_time)
                    return

                elif rpc_call == "10":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("========================")
                    print("Executando teste unitário de adicionar cliente...")

                    clientId = 'Teste'
                    nome = "Cliente"
                    sobrenome = "Teste"
                    dadosCliente = {"nome": nome, "sobrenome": sobrenome}

                    request = admin_pb2.inserirClienteRequest(clientId=clientId, dadosCliente=json.dumps(dadosCliente))
                    reply = stub.inserirCliente(request)

                    if reply.message == 'Cliente inserido!':
                        print("Teste unitário bem-sucedido! Cliente de teste inserido.")
                    else:
                        print("Teste unitário falhou! Erro ao inserir cliente de teste.")

                    sleep(sleep_time)
                else:
                    print("Serviço inválido!")
    except:
        os.system('cls')
        print(
            "======== ERRO! ========\n Possivelmente a porta informada não está configurada como servidor...\nTente novamente  com outra porta...")


if __name__ == "__main__":
    run()
