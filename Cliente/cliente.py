import os

import client_pb2_grpc
import client_pb2
import grpc
from time import sleep

def run():
    sleep_time = 0.8
    print("===================================")
    porta = input("Digite uma porta para se conectar ao servidor: ")
    os.system('cls' if os.name == 'nt' else 'clear')
    with grpc.insecure_channel(f'localhost:{porta}') as channel:
        stub = client_pb2_grpc.ClientStub(channel)
        selection_string = ("\t PAINEL CLIENTE\n"
                            "1. Criar Pedido\n"
                            "2. Modificar Pedido\n"
                            "3. Listar Pedido\n"
                            "4. Listar Pedidos\n"
                            "5. Apagar Pedido\n"
                            "6. Sair\n")

        while True:
            os.system('cls')
            rpc_call = input(selection_string + "\nSelecione um serviço: ")
            if rpc_call == "1":
                clientId = input("Digite o ID (Cliente):")
                request = client_pb2.criarPedidoRequest(clientId=clientId)
                reply = stub.criarPedido(request)
                print(reply.message)
                sleep(sleep_time)
            elif rpc_call == "2":
                clientId = input("Digite o ID (Cliente) :")
                produto = input("Nome do produto:")
                ordemId = input("Ordem:")
                quantidade = int(input("Digite a quantidade do produto:"))
                request = client_pb2.modificarPedidoRequest(clientId=clientId, ordemId=ordemId, produto=produto,
                                                            quantidade=quantidade)
                reply = stub.modificarPedido(request)
                print(reply.message)
                sleep(sleep_time)
            elif rpc_call == "3":
                clientId = input("Digite o ID (Cliente) :")
                ordemId = input("Ordem:")
                request = client_pb2.listarPedidoRequest(clientId=clientId, ordemId=ordemId)
                reply = stub.listarPedido(request)
                print(reply.message)
                sleep(sleep_time)
            elif rpc_call == "4":
                clientId = input("Digite o ID (Cliente) :")
                request = client_pb2.listarPedidosRequest(clientId=clientId)
                reply = stub.listarPedido(request)
                print(reply.message)
                sleep(sleep_time)
            elif rpc_call == "5":
                clientId = input("Digite o ID (Cliente) :")
                ordemId = input("Ordem:")
                request = client_pb2.apagarPedidoRequest(clientId=clientId, ordemId=ordemId)
                reply = stub.apagarPedido(request)
                print(reply.message)
                sleep(sleep_time)
            elif rpc_call == "6":
                print("Portal finalizado..")
                sleep(sleep_time)
                break
            else:
                print("Serviço inválido!")


if __name__ == "__main__":
    run()