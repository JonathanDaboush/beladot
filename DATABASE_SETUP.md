# Database Configuration

This project uses **two separate PostgreSQL databases** to avoid conflicts between live development and testing:

## 📊 Database Separation

| Database | Purpose | Used By | Connection |
|----------|---------|---------|------------|
| **`divina_dev`** | Live/Development Server | `docker-compose up`, main app | `postgresql://postgres:password@localhost:5432/divina_dev` |
| **`divina_test`** | Testing | `pytest` (when using Postgres) | `postgresql://postgres:password@localhost:5432/divina_test` |

## 🚀 Live Server (divina_dev)

The **live development server** always uses `divina_dev`:

```bash
# Start the live server
docker-compose up

# Backend connects to: divina_dev
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# PostgreSQL: localhost:5432
```

**Connection in pgAdmin:**
- Host: `localhost`
- Port: `5432`
- Database: **`divina_dev`** ← This is where your live data is!
- Username: `postgres`
- Password: `password`

## 🧪 Testing (divina_test)

**Tests use SQLite in-memory by default** (no Postgres required), but you can use Postgres for testing:

### Option 1: SQLite (Default)
```bash
pytest  # Uses in-memory SQLite automatically
```

### Option 2: Postgres (divina_test)
```bash
# First, create the test database
docker exec beladot-postgres-1 psql -U postgres -c "CREATE DATABASE divina_test;"

# Run tests with Postgres
export TEST_DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/divina_test"
pytest
```

## 🔧 Configuration Files

- **`backend/config.py`**:
  - `DevelopmentSettings` → `divina_dev`
  - `TestSettings` → `divina_test`
  
- **`docker-compose.yml`**:
  - Creates `divina_dev` database automatically
  
- **`backend/tests/conftest.py`**:
  - Uses SQLite by default
  - Respects `TEST_DATABASE_URL` for Postgres testing

## 📝 Notes

- **Never run tests against `divina_dev`** - this could corrupt your development data
- The test database (`divina_test`) is **not created automatically** - create it manually if needed
- All 34 demo accounts are seeded into `divina_dev` on startup
- Use `scripts/reset_test_db.py` to reset the test database (divina_test)
