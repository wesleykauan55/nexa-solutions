# Repositório-base — Nexa Solutions

> Projeto didático para a disciplina de **Manutenção e Evolução de Software**.

## Contexto

A Nexa Solutions mantém uma API de chamados internos. A empresa precisa corrigir problemas relatados por usuários, melhorar a execução em diferentes ambientes e implementar funcionalidades solicitadas pela coordenação de suporte.

A aplicação registra chamados com título, descrição e status. O backend foi desenvolvido com Django e Django REST Framework, com uma página HTML simples para consumo da API.

## Tecnologias

* Python 3.12
* Django
* Django REST Framework
* SQLite
* Docker
* Docker Compose
* Git

## O que já existe

* API REST para listar e cadastrar chamados.
* API para consultar e atualizar chamados.
* Modelo `Chamado`.
* Interface HTML simples para consumo da API.
* Configuração inicial para Docker.
* Testes automatizados.
* Migrações do banco de dados.
* Lista de demandas da empresa em [`docs/issues.md`](docs/issues.md).

## Estrutura do projeto

```text
nexa-solutions/
├── backend/
│   ├── config/
│   ├── chamados/
│   │   ├── migrations/
│   │   ├── test/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   └── index.html
├── docs/
│   ├── issues.md
│   └── README.md
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Pré-requisitos

### Execução local

Para executar o projeto localmente, é necessário ter:

* Python 3.12 ou compatível;
* Git.

### Execução com Docker

Para executar o projeto utilizando containers, é necessário ter:

* Docker;
* Docker Compose.

## Configuração das variáveis de ambiente

O projeto possui o arquivo `.env.example`, que serve como modelo para configuração das variáveis de ambiente.

Na raiz do projeto, crie o arquivo `.env` a partir do exemplo.

### Windows PowerShell

```powershell
Copy-Item .env.example .env
```

### Linux/macOS

```bash
cp .env.example .env
```

Depois, abra o arquivo `.env` para conferir ou ajustar os valores.

> **Importante:** não versione o arquivo `.env`. Ele pode conter informações sensíveis. O arquivo `.env.example` deve ser utilizado como modelo de configuração.

> **Observação:** a configuração atual do projeto utiliza SQLite. As variáveis relacionadas ao PostgreSQL presentes no `.env.example` fazem parte da preparação para uma futura etapa de integração com PostgreSQL.

## Execução local

Entre na pasta do backend:

```bash
cd backend
```

Crie um ambiente virtual:

### Windows PowerShell

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute as migrações:

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver
```

A aplicação ficará disponível em:

```text
http://localhost:8000/
```

A API de chamados estará disponível em:

```text
http://localhost:8000/api/chamados/
```

## Execução com Docker

O projeto possui arquivos de configuração para execução utilizando Docker e Docker Compose.

Para utilizar essa opção, é necessário ter o Docker instalado e disponível no terminal.

Na raiz do projeto, execute:

```bash
docker compose build
```

Depois:

```bash
docker compose up
```

Ou, para executar os containers em segundo plano:

```bash
docker compose up -d
```

Para acompanhar os logs:

```bash
docker compose logs -f
```

Para parar os serviços:

```bash
docker compose down
```

### Migrações utilizando Docker

Quando o container estiver em execução, as migrações podem ser executadas com:

```bash
docker compose exec api python manage.py migrate
```

> **Importante:** a configuração Docker atual é inicial e ainda possui limitações de infraestrutura. A integração com banco de dados PostgreSQL e os demais ajustes necessários para uma execução completamente reproduzível fazem parte das demandas futuras do projeto.

## Testes

Os testes automatizados da aplicação estão localizados em:

```text
backend/chamados/test/test_chamados.py
```

Para executar os testes localmente, entre na pasta `backend`:

```bash
cd backend
```

Com o ambiente virtual ativado, execute:

```bash
python manage.py test chamados
```

Para executar todos os testes do projeto:

```bash
python manage.py test
```

Os testes incluem a validação do cadastro de chamados, incluindo a obrigatoriedade do campo `titulo`.

## API

A API utiliza Django REST Framework.

### Principais endpoints

| Método  | Endpoint              | Descrição                        |
| ------- | --------------------- | -------------------------------- |
| `GET`   | `/api/chamados/`      | Lista todos os chamados          |
| `POST`  | `/api/chamados/`      | Cria um novo chamado             |
| `GET`   | `/api/chamados/<id>/` | Consulta um chamado específico   |
| `PUT`   | `/api/chamados/<id>/` | Atualiza um chamado específico   |
| `PATCH` | `/api/chamados/<id>/` | Atualiza parcialmente um chamado |

### Listar chamados

```http
GET /api/chamados/
```

Retorna a lista de chamados cadastrados.

Os registros são retornados ordenados pelos mais recentes.

### Criar chamado

```http
POST /api/chamados/
Content-Type: application/json
```

Exemplo:

```json
{
    "titulo": "Computador não liga",
    "descricao": "O computador do setor financeiro não está iniciando.",
    "status": "aberto"
}
```

O campo `titulo` é obrigatório e não pode ser vazio.

### Consultar chamado

```http
GET /api/chamados/1/
```

Substitua `1` pelo ID do chamado desejado.

### Atualizar chamado

```http
PUT /api/chamados/1/
```

Atualiza os dados do chamado informado.

### Atualização parcial

```http
PATCH /api/chamados/1/
```

Permite alterar parcialmente os dados do chamado.

## Campos do chamado

| Campo           | Descrição                            |
| --------------- | ------------------------------------ |
| `id`            | Identificador do chamado             |
| `titulo`        | Título do chamado                    |
| `descricao`     | Descrição do problema ou solicitação |
| `status`        | Status atual do chamado              |
| `criado_em`     | Data e hora de criação               |
| `atualizado_em` | Data e hora da última atualização    |

Os campos `id`, `criado_em` e `atualizado_em` são preenchidos automaticamente pela aplicação.

## Respostas HTTP

A API utiliza códigos HTTP para indicar o resultado das requisições.

| Código            | Significado                       |
| ----------------- | --------------------------------- |
| `200 OK`          | Requisição processada com sucesso |
| `201 Created`     | Recurso criado com sucesso        |
| `400 Bad Request` | Dados enviados são inválidos      |
| `404 Not Found`   | Recurso não encontrado            |

## Frontend

O projeto possui uma interface HTML simples em:

```text
frontend/index.html
```

A interface permite consumir a API para consultar e cadastrar chamados.

## Demandas do projeto

As demandas e problemas relatados pela empresa estão documentados em:

[`docs/issues.md`](docs/issues.md)

Cada demanda deve ser desenvolvida em uma branch própria e integrada à `main` por meio de Pull Request.

## Fluxo de desenvolvimento

Para iniciar uma nova demanda, crie uma branch a partir da `main`:

```bash
git checkout main
git pull origin main
git checkout -b feature/nome-da-tarefa
```

Após realizar as alterações:

```bash
git status
git add .
git commit -m "Descrição da alteração"
git push origin feature/nome-da-tarefa
```

Depois, abra um Pull Request para a branch `main`.

Antes de solicitar o merge, execute os testes:

```bash
python manage.py test chamados
```

## Status do projeto

O projeto está sendo evoluído gradualmente conforme as demandas descritas em `docs/issues.md`.

Algumas melhorias de infraestrutura e funcionalidades ainda fazem parte das próximas etapas do projeto, incluindo a integração com PostgreSQL e a evolução da configuração Docker.
