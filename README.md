# 📦 Local Services Orchestration

## Descrição

Após passar horas controlando via terminal meus microserviços separadamente, ou as vezes até com ajunda de um
script de shell que deixava o trabalho menos manual, resolvi automatizar esse processo com este pequeno projeto python.
Agora com apenas um comando e poucos parâmetros no terminal, todos os microserviços necessários para um
teste sobem automaticamente e na orderm e dependência necessária se for o caso.

## 🚀 Principais Funcionalidades

- Iniciar vários serviços: Em um único comando inicie todos seus microserviços necessários.
- Controle de dependências: configure a ordem que os serviços devem ser iniciados.
- Controle de quantidade: É possível desabilitar e habilitar quais serviços devem iniciar ou não conforme o teste precisa.

## 🛠️ Tecnologias Utilizadas

### Linguagens

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📦 Pré-requisitos

Skaffold [link](https://skaffold.dev/)

## 🚀 Instalação

1. Clone o repositório
```bash
git clone https://github.com/henriquemanduca/local-service-manager
```

## 🔧 Configuração

Faça uma copia do arquivo sample_ms_configuration.yml (o nome do arquivo deve ser ms_configuration.yml).
Configure todos os serviços que deseja controlar, se atentando as dependencias se for necessário.

```yml
projeto1:
  dependencies: []
  enabled: true
  path: folder-name
  port: 8080
projeto2:
  dependencies:
  - projeto1
  enabled: true
  path: folder-name
  port: 8082
...
```

## 📝 Uso

No terminal, execute o arquivo principal conforme exemplo:

```shell
./ms_orchestration.py -d /home/user/projetos/ms --disable project3 --enable project2 --save
```

## 📊 Status do Projeto

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 📧 Contato

Henrique Manduca - [LinkedIn](https://www.linkedin.com/in/henrique-manduca)
