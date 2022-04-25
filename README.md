# PBL-REDES 1 Coleta de Lixo Inteligente

## 📁 Acesso ao projeto
Você pode acessar os arquivos do projeto clicando [aqui](https://github.com/WesleiSantos/PBL-REDES-TCP.git).

## ✔️ Técnicas e tecnologias utilizadas

- ``python``
- ``sockets``
- ``mysql``
- ``docker``
- ``VScode``
- ``linux``

## 🛠️ Abrir e rodar o projeto

### Setup
Para instalar e configurar o docker no ubuntu acesse [aqui](https://docs.docker.com/engine/install/ubuntu/)

Para o container poder acessar a GUI, talvez seja necessário rodar o comando no terminal
-   xhost +

Para criar a imagem e rodar o app é necessário acessar o diretório desejado e rodar o comando:
-  docker-compose up --build
```
cd Servidor
docker-compose up --build
```

Para de excluir é necessário rodar o comando:
-  docker-compose down -v
```
cd Servidor
docker-compose down -v
```

## FUNCIONALIDADES

## Lixeira
-   Insira o host e porta do servidor e as cordenadas e capacidade de uso.
#### Função
-   Colocar e retirar lixo.

## Caminhão
-   Insira o host e porta do servidor e as cordenadas iniciais e capacidade de uso.
#### Função
-   Coletar lixo.

## Admin
-   Insira o host e porta do servidor.
#### Função
-   Bloquear/liberar lixeiras, alterar ordem de coleta, acompanhar em tempo real.

