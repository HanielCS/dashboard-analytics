# 📊 Dashboard Executivo Full Stack

Um sistema completo de gestão e análise de vendas, desenvolvido com arquitetura de microsserviços utilizando Docker. O projeto apresenta um dashboard interativo com gráficos, KPIs, filtragem avançada e previsão de vendas futuras baseada em IA (ARIMA).

## 🚀 Funcionalidades Principais

### 1. Gestão de Vendas (CRUD)

* **Criar, Editar e Deletar** vendas diretamente pela interface.
* Validação de formulários e feedback visual com Toasts (Notificações).
* Confirmação via Modal antes de ações destrutivas (Excluir).

### 2. Inteligência de Dados (BI & AI)

* **KPIs Dinâmicos:** Comparação automática com o período anterior (ex: "⬆ 15% vs mês passado").
* **Predição de Vendas (ARIMA):** Algoritmo de Machine Learning que analisa o histórico e projeta a tendência para os próximos 7 dias.
* **Análise por Categoria:** Gráfico de rosca interativo para visualizar a distribuição de receita.

### 3. Performance & Escalabilidade

* **Cache com Redis:** Acelera o carregamento do dashboard armazenando consultas frequentes.
* **Paginação Server-Side:** Lida eficientemente com grandes volumes de dados.
* **Processamento em Segundo Plano (Celery + RabbitMQ):** Importação de arquivos grandes sem travar a interface.

### 4. Importação e Exportação

* **Importação em Massa:** Upload de ficheiros CSV processados assincronamente.
* **Exportação de Relatórios:** Geração de PDF e Excel filtrados por período.

### 5. Observabilidade

* **Monitoramento:** Métricas em tempo real (RPS, Latência) com Prometheus e Grafana.

## 🛠️ Arquitetura do Projeto

O sistema é orquestrado via Docker Compose e dividido nos seguintes serviços:

| Serviço | Tecnologia | Porta | Descrição |
| :--- | :--- | :--- | :--- |
| **Frontend** | Vue.js 3 + Vite | 8080 | SPA (Single Page Application) reativa. |
| **Backend** | FastAPI (Python) | 8000 | API REST, Regras de Negócio e IA. |
| **Database** | PostgreSQL 15 | 5432 | Armazenamento persistente de dados. |
| **Cache** | Redis | 6379 | Cache de consultas e Broker do Celery. |
| **Queue** | RabbitMQ | 5672 | Fila de mensagens para tarefas assíncronas. |
| **Worker** | Celery | - | Processador de tarefas em background (ex: Import CSV). |
| **Monitor** | Prometheus | 9090 | Coletor de métricas da API. |
| **Visualizer** | Grafana | 3000 | Dashboards de infraestrutura e aplicação. |

## 📦 Como Rodar o Projeto

**Pré-requisitos**

* Docker e Docker Compose instalados na máquina.

**Passo a Passo**

1. **Clone o repositório:**

```bash
git clone https://github.com/HanielCS/dashboard-analytics.git
cd dashboard-analytics
```

2. **Suba o ambiente (Build & Run):** Este comando baixa as imagens, constrói o backend/frontend e inicia todos os serviços.

```bash
docker-compose up --build
```

Acesse o Aplicativo:

* **Dashboard:** [http://localhost:8080](http://localhost:8080)
* **API Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Grafana (Monitoramento):** [http://localhost:3000](http://localhost:3000) *(Login: admin / admin)*
* **RabbitMQ (Filas):** [http://localhost:15672](http://localhost:15672) *(Login: guest / guest)*

## ✅ Testes Automatizados

O projeto possui uma suíte completa de testes integrada ao CI/CD.

### 1. Testes E2E (End-to-End) com Cypress

Simula um utilizador real criando, filtrando e apagando uma venda.

```bash
docker-compose up e2e
```

### 2. Testes Unitários (Backend)

Testa as rotas da API e a lógica de negócio com pytest.

```bash
docker-compose exec backend-service python -m pytest
```

### 3. Testes de Componente (Frontend)

Testa a renderização e lógica dos componentes Vue com vitest.

```bash
docker run --rm -v $(pwd)/frontend:/app -w /app node:22-alpine npm run test -- --run
```

## 📂 Estrutura de Diretórios

```bash
.
├── backend/                        # Código do Backend (API, Lógica de Negócio)
│   ├── services/                   # Lógica de Negócio (Separada por domínio)
│   ├── tests/                      # Testes Automatizados do Backend
│   ├── database.py                 # Configuração de Conexão com Banco (SQLModel) e Cache (Redis)
│   ├── Dockerfile                  # Receita para construir a imagem Docker do Backend (Multi-stage)
│   ├── main.py                     # Ponto de entrada da API FastAPI (Configuração do App, CORS, Instrumentação)
│   ├── requirements.txt            # Lista de dependências Python (FastAPI, Pandas, Celery, etc.)
├── e2e/                            # Testes End-to-End (Cypress)
│   ├── cypress.config.js           # Configuração do Cypress (URL base, viewport)
│   └── Dockerfile                  # Receita para construir o container de teste (com Cypress e Browsers)
├── frontend/                       # Código do Frontend (Vue.js)
│   ├── src/assets/styles/          # Estilização
│   │   ├── components/             # Componentes Vue Reutilizáveis
│   │   ├── services/               # Comunicação com API e Lógica de Frontend
│   │   ├── App.vue                 # Componente Raiz (Layout Principal)
│   │   └── main.js                 # Ponto de entrada do Vue (Monta a app e importa CSS)
│   └── Dockerfile                  # Receita para construir a imagem do Frontend (Multi-stage Node -> Nginx/Dev)
├── prometheus/prometheus.yml       # Configuração de Monitoramento
└── docker-compose.yml              # Orquestração de todos os serviços (Backend, Frontend, BD, Redis, RabbitMQ, Worker, Monitoramento)
```

## 📝 Licença

Este projeto foi desenvolvido para fins de estudo e portfólio. Sinta-se à vontade para usar como base para seus próprios projetos.
