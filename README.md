# Projeto de Sistemas Distribuídos

Este projeto é uma implementação de um sistema distribuído que inclui um painel de administrador e um painel de cliente para listagem de produtos. Este arquivo README contém instruções passo a passo sobre como executar o código e acessar os paineis.

## Pré-requisitos

Certifique-se de ter instalado:

- Python 3.11

## Instruções para executar o código
### Administrador
Siga os passos abaixo para executar o código e acessar o painel do administrador.

1. Abra o terminal e navegue até a pasta do projeto.

2. Acesse a pasta Administrador utilizando o comando:
**cd Administrador**

3. Execute o script `admin_server.py` usando o comando:
**python admin_server.py**

4. Agora, o servidor do administrador está em execução. Para acessar o painel do administrador, abra um novo terminal.

5. No novo terminal, navegue até a pasta do projeto e acesse novamente a pasta Administrador utilizando o comando:
**cd Administrador**

6. Execute o script `admin.py` usando o comando:
**python admin.py**
### Cliente
Siga os passos abaixo para executar o código e acessar o painel do cliente.

1. Abra o terminal e navegue até a pasta do projeto.

2. Acesse a pasta Cliente utilizando o comando:
**cd Cliente**

3. Execute o script `client_server.py` usando o comando:
**python client_server.py**

4. Agora, o servidor do cliente está em execução. Para acessar o painel do cliente, abra um novo terminal.

5. No novo terminal, navegue até a pasta do projeto e acesse novamente a pasta Cliente utilizando o comando:
**cd Cliente**

6. Execute o script `cliente.py` usando o comando:
**python client.py**

##Mecanismos de comunicação
Este projeto utiliza diferentes mecanismos de comunicação para estabelecer conexões entre os componentes do sistema. A seguir estão os detalhes dessas conexões:


Entre o `cliente` e o `client_server`: **gRPC** é utilizado como mecanismo de comunicação para proporcionar uma comunicação rápida e eficiente entre o cliente e o servidor.

Entre o `administrador` e o `admin_server`: **gRPC** também é utilizado para estabelecer uma comunicação confiável e de alto desempenho entre o painel do administrador e o servidor.

Entre o `client_server` e o `admin_server`: **MQTT** é utilizado para permitir uma comunicação assíncrona e baseada em eventos entre os servidores, garantindo escalabilidade e eficiência no sistema distribuído.
