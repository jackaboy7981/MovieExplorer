# MovieExplorer

MovieExplorer is a full-stack platform to explore movies, actors, and directors.

The search experience is global: you can search by movie title, contributor names (actors/directors), genres, and release year terms. You can also refine results with filters like release year and genre.

Search results use infinite scrolling (lazy loading): as you scroll down, additional results are fetched automatically and appended to the list.

Each movie has a dedicated page with key details such as title, genres, release year, and contributor information (actors/directors). Each contributor has a dedicated profile page showing their roles and the movies they have worked on.

If you want to verify this behavior, open browser DevTools → Network tab, search with a broad term (for example `a`), and scroll down to see additional paginated `/browse` requests being triggered.

## Run The Project

### Prerequisites
- Docker Desktop (or Docker Engine + Docker Compose) installed

### Start everything
From the project root:

```bash
docker compose up --build
```

This starts:
- Postgres (`db`) on `localhost:5432`
- Backend API (`backend`) on `localhost:8000`
- Frontend (`frontend`) on `localhost:5173`

Once containers are up, open the website at `http://localhost:5173`.

### Run without Docker

#### Prerequisites
- PostgreSQL running locally
- `uv` installed for backend
- Node.js + npm installed for frontend

#### 1) Configure backend environment
Create/update `Backend/.env`:

```env
ENV=dev
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<database_name>
```

#### 2) Start backend
From `Backend/`:

```bash
uv sync
uv run alembic upgrade head
uv run python app/scripts/insert_csv_to_postgres.py --database-url "$DATABASE_URL"
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 3) Start frontend
From `Frontend/`:

```bash
npm install
npm run dev
```

Open `http://localhost:5173`.

## Run Tests

### Backend tests
From `Backend/`:

```bash
uv run python -m pytest app/test -q
```

### Frontend tests
From `Frontend/`:

```bash
npm run test
```

## Linting

Linting tools used:
- Backend: `pylint`
- Frontend: `eslint`

### Backend lint
From `Backend/`:

```bash
uv run pylint app
```

### Frontend lint
From `Frontend/`:

```bash
npm run lint
```

## Data + DB Flow

1. **Migrations** define and create schema using Alembic.
   - Migration files: `Backend/app/migration/versions`
2. **Sample data generation** exists in:
   - `Backend/app/scripts/IMDB_datacollector.py`
   - It scrapes from IMDb endpoints and builds sample CSV data (100 movies set).
3. **Seeding** loads data only when DB tables are empty:
   - `Backend/app/scripts/insert_csv_to_postgres.py`
4. **Container startup** runs this automatically:
   - `Backend/app/scripts/startup.sh`
   - Runs `alembic upgrade head`, then seed script, then starts uvicorn.

## DB Layout

Core tables:
- `title`: movie/title records (`id`, `imdb_reference_id`, `title`, `media_type`, `release_year`)
- `contributor`: people records (`id`, `imdb_reference_id`, `name`)
- `genre_type_lkup`: genre lookup values
- `media_type_lkup`: media type lookup values (currently seeded with `movie`)
- `contributor_type_lkup`: contributor role lookup values (seeded with `actor`, `actress`, `director`)

Mapping tables:
- `title_genre`: many-to-many mapping between `title` and `genre_type_lkup`
- `contributor_title_mapping`: maps contributor + title + role type

Relationship summary:
- One `title` can have many genres and many contributors.
- One `contributor` can be linked to many titles, with one or more roles per title.

## Backend Layout

Base path: `Backend/app`

- `main.py`: FastAPI app setup, CORS, startup/shutdown DB lifecycle
- `controllers/`: request validation + API endpoint handlers
- `service_logic/`: business logic
- `data_providers/`: DB query layer
- `core/`: shared infrastructure (router registration, DB pool, error handling)
- `migration/`: Alembic migration config and versions
- `scripts/`: data collection + seed scripts
- `test/`: pytest tests for controllers and service logic

### Main APIs
- `GET /browse`
  - Query params: `offset`, `page_size`, `search_text`, `release_year`, `genre`
- `GET /browse/genres`
  - Returns available genre options
- `GET /title/{title_id}`
  - Returns title details, genres, and contributors
- `GET /contributor/{contributor_id}`
  - Returns contributor details and associated titles

## Frontend Layout

Base path: `Frontend/src`

- `App.tsx`: route setup + top-level state (theme, home search text)
- `pages/`: page-level screens (`HomePage`, `MoviePage`, `ContributorPage`)
- `components/`: reusable UI (`TopBar`, `Viewer`, `Movie`, `Contributor`)
- `api/`: backend API callers
- `models/`: TS interfaces for API contracts
- `helpers/`: browser storage/helpers (`userDataStorage`)
- `test/`: Vitest + Testing Library tests

### Frontend Routes
- `/` and `/home`: home
- `/movie/:id`: movie detail page (`/movie` redirects home)
- `/contributor/:id`: contributor detail page (`/contributor` redirects home)
- any unknown route redirects home
