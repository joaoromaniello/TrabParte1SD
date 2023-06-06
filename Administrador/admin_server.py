import ast
from concurrent import futures
import grpc
from pysyncobj import SyncObj

import admin_pb2
import admin_pb2_grpc
from paho.mqtt import client as mqtt
import lmdb
import json

mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Admin Server")
client.connect(mqttBroker)

env1 = lmdb.open('/Dados', map_size=1000000)
env2 = lmdb.open('/Dados', map_size=1000000)

dicionarioProduct = dict()
productArray = []


class AdminServicer(admin_pb2_grpc.AdminServicer, SyncObj):

    def get_partition(self, clientId):
        # Converta o clientId para int (se necessário) e aplique o operador modulo
        partition = int(clientId) % 2

        # Retorne a partição correspondente
        if partition == 0:
            return 1, env1  # Insira em env1 se o mod for 0
        else:
            return 2, env2  # Insira em env2 se o mod for 1

    ####FEITO
    def inserirCliente(self, request_iterator, context):
        print("Inserir Cliente")
        reply = admin_pb2.inserirClienteReply()

        # Determinando a partição correta
        partition_number, partition = self.get_partition(request_iterator.clientId)

        # Recuperando dados do banco de dados
        with partition.begin() as txn:
            dadosCliente_db = txn.get(request_iterator.clientId.encode())

        if dadosCliente_db is not None:
            reply.message = 'Cliente já existe!'
        else:
            # Inserindo dados no banco de dados
            with partition.begin(write=True) as txn:
                txn.put(request_iterator.clientId.encode(), request_iterator.dadosCliente.encode())

            client.publish("InserirCliente", str(request_iterator.clientId) + '/' + str(request_iterator.dadosCliente))
            print(
                f"Inserção realizada na partição " + str(
                    partition_number) + f": {request_iterator.clientId}: {request_iterator.dadosCliente}")
            reply.message = f'Cliente inserido na partição  {partition_number}!'

        return reply

    ####FEITO
    def modificarCliente(self, request_iterator, context):
        print("Modificar Cliente")
        reply = admin_pb2.modificarClienteReply()

        # Determinando a partição correta
        partition_number, partition = self.get_partition(request_iterator.clientId)

        # Recuperando dados do banco de dados
        with partition.begin() as txn:
            dadosCliente_db = txn.get(request_iterator.clientId.encode())

        if dadosCliente_db is None:
            reply.message = 'Cliente não existe!'
        else:
            novosDados = json.loads(request_iterator.dadosCliente)
            dadosCliente = {"nome": novosDados['nome'], "sobrenome": novosDados['sobrenome']}
            with partition.begin(write=True) as txn:
                txn.put(request_iterator.clientId.encode(), json.dumps(dadosCliente).encode())

            client.publish("ModificarCliente",
                           str(request_iterator.clientId) + '/' + str(request_iterator.dadosCliente))
            print(
                f"Modificação realizada na partição {partition_number}: {request_iterator.clientId}: {request_iterator.dadosCliente}")
            reply.message = f'Cliente modificado na partição {partition_number}!'

        return reply

    ####FEITO
    def recuperarCliente(self, request_iterator, context):
        print("Recuperar Cliente")
        reply = admin_pb2.recuperarClienteReply()

        # Determinando a partição correta
        partition_number, partition = self.get_partition(request_iterator.clientId)

        # Recuperando dados do banco de dados
        with partition.begin() as txn:
            dadosCliente_db = txn.get(request_iterator.clientId.encode())

        if dadosCliente_db is None:
            reply.message = 'Cliente não existe!'
        else:
            dadosCliente = json.loads(dadosCliente_db)
            reply.message = f"Cliente recuperado na partição {partition_number}:\nNome - {dadosCliente['nome']}\nSobrenome - {dadosCliente['sobrenome']}"

        return reply

    ####FEITO
    def apagarCliente(self, request_iterator, context):
        print("Apagar Cliente")
        reply = admin_pb2.apagarClienteReply()

        # Determinando a partição correta
        partition_number, partition = self.get_partition(request_iterator.clientId)

        # Verificando se o cliente existe
        with partition.begin() as txn:
            dadosCliente_db = txn.get(request_iterator.clientId.encode())

        if dadosCliente_db is None:
            reply.message = 'Cliente não existe!'
        else:
            # Apagando o cliente do banco de dados
            with partition.begin(write=True) as txn:
                txn.delete(request_iterator.clientId.encode())

            client.publish("ApagarCliente", str(request_iterator.clientId))
            print(f"Cliente apagado na partição {partition_number}: {request_iterator.clientId}")
            reply.message = f'Cliente apagado na partição {partition_number}!'

        return reply

    ####FEITO
    def inserirProduto(self, request_iterator, context):
        global dicionarioProduct
        print("Inserir Produto")
        reply = admin_pb2.inserirProdutoReply()
        if request_iterator.produtoId in dicionarioProduct:
            reply.message = 'Produto já existe!'
        else:
            productArray.append([request_iterator.produtoId, request_iterator.dadosProduto])
            dicionarioProduct = dict(productArray)
            client.publish("InserirProduto", str(dicionarioClient) + '/' + str(dicionarioProduct))
            print("Cadastro realizado: " + str(dicionarioProduct))
            reply.message = 'Produto cadastrado!'

        return reply

    ####FEITO
    def modificarProduto(self, request_iterator, context):
        global dicionarioProduct
        print("Modificar Produto")
        reply = admin_pb2.modificarProdutoReply()

        if request_iterator.produtoId not in dicionarioProduct:
            reply.message = 'Produto não existe!'
        else:
            novosDados = json.loads(request_iterator.dadosProduto)
            dadosProduto = {"nome": novosDados['nome'], "quantidade": novosDados['quantidade'],
                            "preco": novosDados['preco']}
            dicionarioProduct[request_iterator.produtoId] = json.dumps(dadosProduto)
            client.publish("ModificarProduto", str(dicionarioClient) + '/' + str(dicionarioProduct))
            print("Modificação realizada: " + str(dicionarioProduct))
            reply.message = 'Produto modificado!'

        return reply

    ####FEITO
    def recuperarProduto(self, request_iterator, context):
        global dicionarioProduct
        print("Recuperar Produto")

        reply = admin_pb2.recuperarProdutoReply()

        if request_iterator.produtoId not in dicionarioProduct:
            reply.message = 'Produto não existe!'
        else:
            dadosProduto = json.loads(dicionarioProduct[request_iterator.produtoId])
            print("Produto recuperado: " + str(dicionarioProduct))
            reply.message = f"Produto recuperado:\nNome - {dadosProduto['nome']}\nQuantidade - {dadosProduto['quantidade']}"

        return reply

    ####FEITO
    def apagarProduto(self, request_iterator, context):
        global dicionarioProduct
        print("Apagar Produto")

        reply = admin_pb2.apagarProdutoReply()

        if request_iterator.produtoId not in dicionarioProduct:
            reply.message = 'Produto não existe!'
        else:
            dicionarioProduct.pop(request_iterator.produtoId)
            client.publish("ApagarProduto", str(dicionarioClient) + '/' + str(dicionarioProduct))
            print("Produto apagado: " + str(dicionarioProduct))
            reply.message = 'Produto apagado!'

        return reply

    def on_message(client, userdata, message):
        print("Produtos cadastrados: ", ast.literal_eval(message.payload.decode("utf-8")))
        global dicionarioProduct
        dicionarioProduct = ast.literal_eval(message.payload.decode("utf-8"))

    def adicionaClienteTeste(self, request, context):
        global dicionarioClient
        print("Adiciona cliente (Teste)")
        reply = admin_pb2.adicionaClienteTesteReply()

        if request.clientId in dicionarioClient:
            reply.message = 'Cliente já existe!'
        else:
            clientArray.append([request.clientId, request.dadosCliente])
            dicionarioClient = dict(clientArray)
            client.publish("adicionaClienteTeste", str(dicionarioClient) + '/' + str(dicionarioProduct))
            print("Inserção realizada (Teste): " + str(dicionarioClient))
            reply.message = 'Cliente inserido (Teste)!'

        return reply

    client.loop_start()
    client.subscribe("ModificarPedido")
    client.subscribe("ApagarPedido")
    client.on_message = on_message


def serve():
    porta = input("Digite a porta para ABRIR o servidor: ")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_pb2_grpc.add_AdminServicer_to_server(AdminServicer(), server)
    server.add_insecure_port(f"localhost:{porta}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
