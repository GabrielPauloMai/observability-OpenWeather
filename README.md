# Projeto de Observabilidade

Este projeto tem como objetivo criar um ambiente de observabilidade usando várias ferramentas, incluindo Prometheus, Alertmanager, Grafana, Cadvisor, MongoDB, Elasticsearch e Graylog. Ele também inclui um container em Python que gera um servidor web local para amostragem de métricas de status code 200 e 401, e outros casos personalizáveis.

## Pré-requisitos

- [Conta da AWS](https://aws.amazon.com/)
- [AWS CLI instalada e configurada](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
- Conhecimento básico de AWS CloudFormation
- [Docker](https://docs.docker.com/get-docker/)
- Acesso à Internet para download de recursos

## Tecnologias

- AWS
- Docker
- Docker Compose
- Prometheus
- Alertmanager
- Grafana
- Graylog


## Como usar

### 1. Implantação da stack na AWS

Use o arquivo CloudFormation fornecido para criar a infraestrutura necessária na AWS. Certifique-se de que o AWS CLI esteja configurado corretamente e, em seguida, execute o seguinte comando:

```bash
aws cloudformation create-stack --stack-name ObservabilityStack --template-body file://observability-stack.yaml
```

### 2. Configuração do container Python

Após a conclusão da implantação, você terá uma instância EC2 com o container Python em execução. Para configurar o container:

- SSH na instância EC2 usando a chave apropriada.

```bash
ssh -i sua-chave.pem ec2-user@seu-endereco-ip
```

- Dentro da instância, navegue até a pasta raiz do projeto:

```bash
cd observability-OpenWeather-master/cloudformation
```

- Execute o script de inicialização:

```bash
./init.sh
```

Isso configurará o ambiente e iniciará o servidor web Python para amostragem de métricas.

### 3. Acesso às ferramentas de observabilidade

Após a conclusão da configuração, você pode acessar as seguintes ferramentas:

- Prometheus: `http://seu-endereco-ip:9090`
- Grafana: `http://seu-endereco-ip:3000` (Usuário: admin, Senha: admin)
- Cadvisor: `http://seu-endereco-ip:8080`
- AlertManager: `http://seu-endereco-ip:9093`

### 4. Configuração do Graylog e Logs

- Graylog: Acesse a interface local do Graylog em `http://seu-endereco-ip:9000`.
- MongoDB e Elasticsearch estão configurados para armazenar logs das aplicações.

### 5. Criação de Dashboards no Grafana

Importe o dashboard do Prometheus:Dashboard -> Import -> Upload JSON file
Selecione o arquivo: dashboard.json -> Selecione o data source: Prometheus -> Import 

![Logo do Meu Projeto](image\screencapture-34-232-72-239-3000-d-a2ac5d88-47c5-48f2-a13d-a944c7f4e32e-open-weather-copy-2023-11-05-18_07_06.png)



## Resultados

O resultado final esperado é configurar um ambiente de observabilidade completo usando as ferramentas mencionadas e criar dashboards no Grafana para monitorar métricas. Além disso, o Graylog deve estar funcionando localmente para evidenciar o funcionamento básico.

## Autores

- Ana Thais, Andresa Trentini, Gabriel Paulo, Lucas Cavalcanti




