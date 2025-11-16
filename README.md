# Python VSCode Settings Validation Project

## 📋 Project Overview

This project is designed to validate and establish optimal VSCode settings for Python development using modern tooling. The primary focus is on testing and documenting the best configuration for:

- **uv**: Fast Python package installer and resolver
- **ruff**: Extremely fast Python linter and formatter
- **pyright**: Static type checker for Python

## 🎯 Project Goals

1. **Tool Validation**: Verify the effectiveness and integration of ruff and pyright in real-world scenarios
2. **VSCode Configuration**: Establish optimal VSCode settings for Python development
3. **Best Practices**: Document configuration patterns and recommended setups
4. **Framework Testing**: Build sample applications using FastAPI, SQLAlchemy, and Prisma to test tooling across different use cases

## 🛠️ Technology Stack

### Core Tools
- **uv**: Package management and virtual environment
- **ruff**: Linting and formatting
- **pyright**: Type checking

### Frameworks & Libraries
- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM (async with aiosqlite)
- **Prisma**: Next-generation ORM with type-safe database client
- **Pydantic**: Data validation using Python type annotations

## 📁 Project Structure (Monorepo)

```
python-vscode-settings/
├── .vscode.example/                         # Example VSCode configuration
│   ├── settings.json                        # Workspace settings
│   ├── extensions.json                      # Recommended extensions
│   ├── tasks.json                           # Development tasks
│   └── launch.json                          # Debug configurations
├── apps/                                    # Applications
│   └── api/                                 # FastAPI application
│       ├── src/                             # API source code
│       │   ├── config.py                    # App configuration
│       │   ├── database.py                  # SQLAlchemy async setup
│       │   ├── main.py                      # FastAPI app entry point
│       │   ├── routers/                     # API route handlers
│       │   │   ├── users.py                 # SQLAlchemy-based endpoints
│       │   │   └── users_prisma.py          # Prisma-based endpoints
│       │   └── schemas/                     # Pydantic schemas
│       ├── tests/                           # Comprehensive test suite
│       │   ├── conftest.py                  # Pytest fixtures
│       │   ├── test_users.py                # SQLAlchemy tests (11 tests)
│       │   └── test_users_prisma.py         # Prisma tests (7 tests)
│       ├── pyproject.toml                   # App dependencies
│       └── .python-version                  # Python 3.10.14
├── packages/                                # Shared packages
│   ├── sqlalchemy/                          # SQLAlchemy models package
│   │   ├── src/
│   │   │   └── my_sqlalchemy/               # Explicit namespace
│   │   │       ├── __init__.py              # Package exports
│   │   │       └── models/                  # Database models
│   │   │           ├── __init__.py
│   │   │           ├── base.py              # Declarative base
│   │   │           └── user.py              # User model (async)
│   │   └── pyproject.toml                   # SQLAlchemy 2.0+ dependency
│   └── prisma/                              # Prisma ORM package
│       ├── schema.prisma                    # Prisma schema definition
│       ├── migrations/                      # Database migrations
│       ├── src/
│       │   └── my_prisma/                   # Explicit namespace
│       │       ├── __init__.py              # Prisma client wrapper
│       │       ├── client.py                # Prisma client instance
│       │       └── manager.py               # PrismaManager singleton
│       └── pyproject.toml                   # Prisma dependency
├── pyproject.toml                           # Workspace & tool config
├── pyrightconfig.json                       # Pyright configuration
├── .python-version                          # Python 3.10.14
├── uv.lock                                  # Dependency lock file
└── README.md                                # This file
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) installed

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd python-vscode-settings
```

2. **Install all workspace dependencies**
```bash
uv sync --all-groups
```

This will:
- Create `.venv` in project root
- Install all dependencies from workspace and apps
- Generate `uv.lock` file

3. **Activate virtual environment**
```bash
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

4. **Setup VSCode configuration**
```bash
cp -r .vscode.example .vscode
```

5. **Open in VSCode**
```bash
code .
```

## ⚙️ Configuration Goals

### VSCode Settings
The `.vscode/settings.json` (copied from `.vscode.example/`) includes:
- ✅ Automatic formatting on save using ruff
- ✅ Real-time type checking with pyright (via Pylance)
- ✅ Intelligent code completion
- ✅ Import organization
- ✅ Path resolution for monorepo structure
- ✅ Pytest integration for all apps

### VSCode Tasks
The `.vscode/tasks.json` provides common development commands:
- `uv: sync` - Install/update dependencies
- `ruff: format` - Format all code
- `ruff: check` - Lint code
- `ruff: check --fix` - Auto-fix linting issues
- `pytest: run all` - Run all tests
- `pytest: run with coverage` - Run tests with coverage report
- `pyright: check` - Type check entire project
- `uvicorn: run dev server` - Start FastAPI development server

Access via: `Cmd+Shift+P` → "Tasks: Run Task"

### VSCode Debugging
The `.vscode/launch.json` provides debug configurations:
- `FastAPI: Run API Server` - Debug FastAPI with auto-reload
- `FastAPI: Run API Server (No Reload)` - Debug FastAPI without reload
- `Python: Current File` - Debug currently open Python file
- `Pytest: Current File` - Debug tests in current file
- `Pytest: All Tests` - Debug all tests

Access via: `F5` or Debug panel (`Cmd+Shift+D`)

### Ruff Configuration
Root-level configuration for entire monorepo:
- ✅ Python 3.10 target version
- ✅ 100 character line length
- ✅ Comprehensive rule sets (E, W, F, I, N, UP, ANN, B, PL, etc.)
- ✅ Auto-fix enabled for all rules
- ✅ Integration with VSCode formatter

### Pyright Configuration
Workspace-aware type checking:
- ✅ Basic type checking mode
- ✅ Monorepo-aware execution environments
- ✅ Path resolution for apps and packages
- ✅ Integration with FastAPI and SQLAlchemy types
- ✅ Custom stub path support

## 📝 Development Workflow

1. **Phase 1**: Basic setup and tool configuration ✅
   - Monorepo structure with uv workspace
   - Ruff and Pyright configuration
   - VSCode settings and extensions
   - Development tasks and debug configurations

2. **Phase 2**: Shared packages and models ✅
   - `packages/sqlalchemy` with async SQLAlchemy 2.0 models
   - User model with type-safe mapped columns
   - Explicit `my_sqlalchemy` namespace

3. **Phase 3**: FastAPI application ✅
   - Complete CRUD API endpoints
   - Async database integration with SQLAlchemy
   - Pydantic schemas for validation
   - Comprehensive test suite (11 tests)
   - All tests passing with pytest-asyncio

4. **Phase 4**: Prisma integration ✅
   - Prisma schema matching SQLAlchemy models
   - Complete Prisma-based API endpoints (`/api/v1/prisma/users`)
   - Database migrations with Prisma Migrate
   - Comprehensive Prisma test suite (7 tests)
   - PrismaManager singleton for client lifecycle management
   - Side-by-side comparison capability

5. **Phase 5**: API optimization ✅
   - Differential response schemas (list vs detail endpoints)
   - Query optimization for list endpoints
   - SQLAlchemy: Field-level SELECT for minimal data transfer
   - Prisma: Python-level field filtering (DB-level select not supported)

6. **Phase 6**: Documentation and comparison (In Progress)
   - SQLAlchemy vs Prisma comparison
   - Performance benchmarks
   - Developer experience analysis

## 🧪 Testing Strategy

### Current Test Coverage
- **Total Tests**: 18 (all passing)
  - SQLAlchemy endpoints: 11 tests
  - Prisma endpoints: 7 tests
- **Test Framework**: pytest with pytest-asyncio
- **Coverage Tools**: pytest-cov with HTML reports
- **Database**: In-memory SQLite for SQLAlchemy, file-based for Prisma

### Test Categories
- **CRUD Operations**: Create, Read, Update, Delete for both ORMs
- **Validation**: Duplicate email/username handling
- **Error Cases**: 404 not found, 400 bad request
- **Pagination**: List operations with skip/limit
- **Async Patterns**: Full async/await testing with proper fixtures

### Running Tests
```bash
# Run all tests
uv run pytest apps/api/tests/ -v

# Run with coverage
uv run pytest apps/api/tests/ --cov=src --cov-report=html

# Run specific test file
uv run pytest apps/api/tests/test_users.py -v
uv run pytest apps/api/tests/test_users_prisma.py -v
```

## 🎯 API Endpoints

### SQLAlchemy Endpoints
Base path: `/api/v1/users`

- `POST /` - Create new user (returns full user details)
- `GET /{user_id}` - Get user by ID (returns full user details)
- `GET /` - List users with pagination (returns minimal fields: id, username, created_at)
- `PATCH /{user_id}` - Update user (returns full user details)
- `DELETE /{user_id}` - Delete user

### Prisma Endpoints
Base path: `/api/v1/prisma/users`

- `POST /` - Create new user (returns full user details)
- `GET /{user_id}` - Get user by ID (returns full user details)
- `GET /` - List users with pagination (returns minimal fields: id, username, created_at)
- `PATCH /{user_id}` - Update user (returns full user details)
- `DELETE /{user_id}` - Delete user

### Response Schema Optimization

The API uses different Pydantic schemas for list and detail endpoints:

**List Response** (`UserListItem`):
```json
{
  "id": 1,
  "username": "testuser",
  "created_at": "2024-11-16T08:00:00"
}
```

**Detail Response** (`UserResponse`):
```json
{
  "id": 1,
  "email": "test@example.com",
  "username": "testuser",
  "full_name": "Test User",
  "is_active": true,
  "created_at": "2024-11-16T08:00:00",
  "updated_at": "2024-11-16T08:00:00"
}
```

**Query Optimization**:
- **SQLAlchemy**: Uses field-level SELECT to fetch only required columns from database
  ```python
  select(User.id, User.username, User.created_at)
  ```
- **Prisma**: Fetches full records from database, filters fields at Python level
  - Prisma Python Client (v0.11.0) does not support dynamic `select` parameter
  - TypeScript/JavaScript Prisma supports `select: { id: true, username: true }`
  - Python implementation uses full record retrieval with post-processing

### Running the API
```bash
# Navigate to API directory
cd apps/api

# Start development server with auto-reload
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or use VSCode debug configuration (F5)
# Select "FastAPI: Run API Server"

# API will be available at:
# - http://localhost:8000
# - Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Environment Configuration
```bash
# Create .env file in apps/api/
cd apps/api
cp .env.example .env

# Edit .env to configure database path
# DB_PATH=./app.db  # Path to SQLite database (used by both SQLAlchemy and Prisma)
```

## 📚 Documentation

Documentation covers:
- ✅ VSCode extension recommendations (`.vscode.example/extensions.json`)
- ✅ Workspace settings configuration (`.vscode.example/settings.json`)
- ✅ Development tasks (`.vscode.example/tasks.json`)
- ✅ Debug configurations (`.vscode.example/launch.json`)
- ✅ Tool-specific configurations (ruff, pyright, pytest)
- ✅ Environment configuration (`.env.example`)
- ⏳ SQLAlchemy vs Prisma comparison (In Progress)
- ⏳ Performance benchmarks (Planned)

## 🔍 Key Learnings

### Monorepo Package Structure
Both SQLAlchemy and Prisma packages follow consistent `src` layout:
```
packages/{package-name}/
├── src/
│   └── my_{package-name}/    # Explicit namespace prevents conflicts
│       ├── __init__.py
│       └── ...
└── pyproject.toml            # packages = ["src"]
```

### Prisma Python Client Limitations
**Important**: Prisma Python Client (v0.11.0) has different capabilities than TypeScript/JavaScript version:

❌ **Not Supported**:
- Dynamic `select` parameter for field selection
  ```python
  # This does NOT work in Python (works in TypeScript)
  await prisma.user.find_many(
      select={"id": True, "username": True}
  )
  ```

✅ **Current Workaround**:
- Fetch full records, filter at Python level
  ```python
  users = await prisma.user.find_many()
  return [{"id": u.id, "username": u.username} for u in users]
  ```

✅ **Alternative** (Complex):
- Use Partial Types (requires pre-defined classes)
- More complex to maintain and not recommended for simple use cases

**SQLAlchemy Advantage**: Supports field-level SELECT for true query optimization
```python
# SQLAlchemy can select specific columns
select(User.id, User.username, User.created_at)
```

### Database Path Management
- Single `DB_PATH` environment variable for both ORMs
- Absolute path calculation from file location prevents working directory issues
- Shared database file ensures consistency across SQLAlchemy and Prisma endpoints

## 🤝 Contributing

This is a validation project. Feedback on configurations and best practices is welcome.

## 📄 License

MIT License

## 🔗 Resources

### Tools
- [uv Documentation](https://github.com/astral-sh/uv) - Fast Python package manager
- [ruff Documentation](https://docs.astral.sh/ruff/) - Extremely fast Python linter
- [pyright Documentation](https://github.com/microsoft/pyright) - Static type checker

### Frameworks
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/) - Python SQL toolkit and ORM
- [Prisma Documentation](https://www.prisma.io/docs) - Next-generation ORM
- [Pydantic Documentation](https://docs.pydantic.dev/) - Data validation library

### Testing
- [pytest Documentation](https://docs.pytest.org/) - Testing framework
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - Asyncio support for pytest
