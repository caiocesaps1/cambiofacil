# CâmbioFácil

Buscador de taxas de câmbio que compara em tempo real as cotações de **USD** e **EUR** entre bancos, fintechs, corretoras e casas de câmbio — ajudando viajantes a encontrar o melhor preço antes de comprar moeda estrangeira.

## Funcionalidades

- Comparação em tempo real de múltiplas instituições financeiras
- Ordenação automática do melhor para o pior câmbio
- Filtro por tipo de instituição (banco, fintech, corretora, casa de câmbio)
- Link direto para compra na instituição selecionada
- Cache de 15 minutos para performance (Redis com fallback in-memory)
- Indicador de última atualização das taxas

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS |
| Data fetching | TanStack Query |
| Backend | Python 3.12 + FastAPI |
| Cache | Redis (fallback: in-memory) |
| Scraping | httpx + BeautifulSoup |
| Infra | Docker + Docker Compose |

## Fontes de dados

| Instituição | Tipo | Método |
|---|---|---|
| Câmbio Oficial (BCB) | Banco | AwesomeAPI (REST) |
| Wise | Fintech | API pública (`/v1/rates`) |
| Nomad | Fintech | httpx + JSON |
| Confidence | Casa de câmbio | httpx + BeautifulSoup |

## Estrutura do projeto

```
cambiofacil/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/rate.py
│   │   ├── routers/rates.py
│   │   └── services/
│   │       ├── cache.py
│   │       ├── fetcher.py
│   │       └── sources/         # awesomeapi, wise, nomad, confidence
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/          # CurrencySelector, AmountInput, FilterBar, RateCard, RateList, LastUpdated
│   │   ├── hooks/useRates.ts
│   │   ├── pages/Home.tsx
│   │   ├── services/api.ts
│   │   └── types/rate.ts
│   ├── nginx.conf
│   └── Dockerfile
└── docker-compose.yml
```

## Rodando localmente

### Com Docker Compose (recomendado)

```bash
docker compose up --build
```

Acesse `http://localhost:3000`

---

### Sem Docker

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Disponível em http://localhost:8000
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
# Disponível em http://localhost:5173
```

> O frontend usa proxy do Vite em dev: `/api/*` → `localhost:8000`

**Redis (opcional)**

```bash
docker run -p 6379:6379 redis:alpine
```

Sem Redis o cache funciona in-memory automaticamente.

## API

### `GET /rates`

Retorna cotações ordenadas do melhor para o pior.

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `currency` | string | sim | `USD` ou `EUR` |
| `amount` | float | não | Valor em BRL (default: `1000.00`) |
| `type` | string | não | `bank`, `fintech`, `broker`, `exchange_house` |

```bash
curl "http://localhost:8000/rates?currency=USD&amount=5000"
```

### `GET /rates/refresh`

Invalida o cache forçando busca fresca na próxima requisição.

### `GET /health`

Retorna `{"status": "ok"}`.

## Variáveis de ambiente

**Backend** (`.env`):

```env
REDIS_URL=redis://localhost:6379
RATE_CACHE_TTL=900
LOG_LEVEL=info
```

**Frontend** (`.env`):

```env
# Necessário apenas em produção. Em dev o proxy do Vite cuida disso.
VITE_API_URL=https://seu-backend.railway.app
```

## Testes

```bash
cd backend
python3 -m pytest tests/ -v
```

15 testes cobrindo o endpoint `/rates`, filtros, erros e todas as fontes (com mocks).
