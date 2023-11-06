# Projeto de Observabilidade

Neste projeto, buscamos estabelecer um robusto ambiente de observabilidade, empregando diversas ferramentas de ponta, tais como Prometheus, Alertmanager, Grafana, Cadvisor, MongoDB, Elasticsearch e Graylog. Para complementar, integramos um contêiner em Python que hospeda um servidor web local, capaz de coletar métricas específicas, como os códigos de status 200 e 401, além de possibilitar cenários personalizáveis.



## Como usar

### 1. Implantação da stack na AWS

Para iniciar o projeto você precisará baixar o arquivo stack.yml e carregá-lo no CloudFormation da AWS.

As configurações serão criadas automaticamente e você poderá acessar sua instância pelo ip público.


### 2. Acesso às ferramentas de observabilidade

Após a conclusão da configuração, você pode acessar as seguintes ferramentas:

- Prometheus: `http://seu-endereco-ip:9090`
- Grafana: `http://seu-endereco-ip:3000` (Usuário: admin, Senha: admin)
- Graylog: `http://seu-endereco-ip:9000`
- AlertManager: `http://seu-endereco-ip:9093`
- Homepage: `http://seu-endereco-ip:5000`

### 3. Configuração do Graylog e Logs

- Graylog: Acesse a interface local do Graylog em `http://seu-endereco-ip:9000`.
- MongoDB e Elasticsearch estão configurados para armazenar logs das aplicações.
Configure o Input do Graylog para receber os logs da Homepage, conforme instruções abaixo:
- System -> Inputs -> Select Input -> GELF TCP -> Launch new input -> Title: Homepage -> Save
 ![GRAYLOG](image\graylog.jpg)

### 4. Criação de Dashboards no Grafana

Importe o dashboard do Prometheus:Dashboard -> Import -> Upload JSON file
Selecione o arquivo: dashboard.json -> Selecione o data source: Prometheus -> Import

![Logo do Meu Projeto](image\screencapture-34-232-72-239-3000-d-a2ac5d88-47c5-48f2-a13d-a944c7f4e32e-open-weather-copy-2023-11-05-18_07_06.png)

### 5. Acesso a Homepage

Acesse a tela inicial da aplicação em `http://seu-endereco-ip:5000`.
Pesquise por uma cidade e clique em "Search". A aplicação irá retornar o clima atual da cidade pesquisada.

![Homepage](image\homepage.jpg)



## Resultados

O resultado final esperado é configurar um ambiente de observabilidade completo usando as ferramentas mencionadas
e criar dashboards no Grafana para monitorar métricas.

Alguns exemplos de logs e métricas que podem ser monitorados:

![logs](image\log1.jpg)
![logs](image\log2.jpg)
![logs](image\log3.jpg)
![logs](image\log4.jpg)



## Autores

- Ana Thais, Andresa Trentini, Gabriel Paulo Mai, Lucas Cavalcanti




