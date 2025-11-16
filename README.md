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
- **SQLModel**: Combines SQLAlchemy ORM with Pydantic validation
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
│       │   ├── database_sqlmodel.py         # SQLModel async setup
│       │   ├── main.py                      # FastAPI app entry point
│       │   ├── routers/                     # API route handlers
│       │   │   ├── users.py                 # SQLAlchemy-based endpoints
│       │   │   ├── users_sqlmodel.py        # SQLModel-based endpoints
│       │   │   └── users_prisma.py          # Prisma-based endpoints
│       │   └── schemas/                     # Pydantic schemas
│       ├── tests/                           # Comprehensive test suite
│       │   ├── conftest.py                  # Pytest fixtures
│       │   ├── test_users.py                # SQLAlchemy tests (11 tests)
│       │   ├── test_users_sqlmodel.py       # SQLModel tests (11 tests)
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
│   ├── sqlmodel/                            # SQLModel package
│   │   ├── src/
│   │   │   └── my_sqlmodel/                 # Explicit namespace
│   │   │       ├── __init__.py              # Package exports
│   │   │       └── models/                  # Database models
│   │   │           ├── __init__.py
│   │   │           └── user.py              # User model (SQLModel + Pydantic)
│   │   └── pyproject.toml                   # SQLModel dependency
│   └── prisma/                              # Prisma ORM package
│       ├── schema.prisma                    # Prisma schema definition (snake_case)
│       ├── prisma/
│       │   └── partial_types.py             # Partial type definitions (generation-time)
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
- Create `.venv` in project root (unified virtual environment for all packages)
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

> **📚 UV Workspace Configuration**: This project uses UV workspace to manage a unified virtual environment across all packages and apps. For detailed information about how `[tool.uv.workspace]`, `[tool.uv.sources]`, and the integrated `.venv` work, see [UV_WORKSPACE_CONFIGURATION.md](UV_WORKSPACE_CONFIGURATION.md).

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

5. **Phase 5**: SQLModel integration ✅
   - `packages/sqlmodel` with SQLModel combining ORM + Pydantic
   - User model with automatic table naming
   - Complete SQLModel-based API endpoints (`/api/v1/sqlmodel/users`)
   - Comprehensive SQLModel test suite (11 tests)
   - Three-way ORM comparison capability (SQLAlchemy, SQLModel, Prisma)

6. **Phase 6**: API optimization ✅
   - Differential response schemas (list vs detail endpoints)
   - Query optimization for list endpoints
   - SQLAlchemy: Field-level SELECT for minimal data transfer
   - SQLModel: Field-level SELECT for minimal data transfer (inherits SQLAlchemy capabilities)
   - Prisma: Field-level SELECT via Partial Types (defined at generation time)

7. **Phase 7**: Documentation and comparison ✅
   - SQLAlchemy vs SQLModel vs Prisma comparison
   - Feature matrix and compatibility analysis
   - Implementation examples and best practices
   - Partial types and query optimization documentation

## 🧪 Testing Strategy

### Current Test Coverage
- **Total Tests**: 29 (all passing)
  - SQLAlchemy endpoints: 11 tests
  - SQLModel endpoints: 11 tests
  - Prisma endpoints: 7 tests
- **Test Framework**: pytest with pytest-asyncio
- **Coverage Tools**: pytest-cov with HTML reports (71% overall coverage)
- **Database**: In-memory SQLite for SQLAlchemy and SQLModel, file-based for Prisma

### Test Categories
- **CRUD Operations**: Create, Read, Update, Delete for all three ORMs
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
uv run pytest apps/api/tests/test_users_sqlmodel.py -v
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

### SQLModel Endpoints
Base path: `/api/v1/sqlmodel/users`

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
- **SQLModel**: Uses field-level SELECT (inherits SQLAlchemy capabilities)
  ```python
  select(User.id, User.username, User.created_at)
  ```
- **Prisma**: Uses Partial Types for field-level SELECT at database level
  ```python
  # Define partial type in prisma/partial_types.py (executed during prisma generate)
  UserMinimal = User.create_partial(
      "UserMinimal",
      include={"id", "username", "created_at"},
  )

  # Use in queries (imports from prisma.partials)
  from prisma.partials import UserMinimal
  users = await UserMinimal.prisma(prisma).find_many()
  ```
  - ✅ **Field-level SELECT supported** via Partial Types (generation-time feature)
  - ❌ Dynamic `select` parameter NOT supported (TypeScript/JavaScript feature only)
  - Partial types defined in `prisma/partial_types.py` and generated during `prisma generate`
  - More verbose than SQLAlchemy/SQLModel but achieves same database-level optimization

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
- ✅ SQLAlchemy vs SQLModel vs Prisma comparison
- ✅ **UV Workspace Configuration** ([UV_WORKSPACE_CONFIGURATION.md](UV_WORKSPACE_CONFIGURATION.md))
  - How UV workspace manages unified virtual environment
  - Detailed pyproject.toml configuration explanation
  - Dependency resolution and editable installation mechanism
  - UV command usage and migration guide
- ⏳ Performance benchmarks (Planned)

## 🔄 ORM Comparison: SQLAlchemy vs SQLModel vs Prisma

### Overview

This project implements the same User CRUD API using three different ORMs to compare their capabilities, limitations, and developer experience.

| Feature | SQLAlchemy 2.0 | SQLModel | Prisma Python |
|---------|----------------|----------|---------------|
| **Type Safety** | ✅ Full (via Mapped) | ✅ Full (via Pydantic) | ✅ Full (generated) |
| **Async Support** | ✅ Native | ✅ Native (inherits) | ✅ Native |
| **Field-level SELECT** | ✅ Supported | ✅ Supported | ✅ **Via Partial Types** |
| **Pydantic Integration** | ⚠️ Manual schemas | ✅ Built-in | ⚠️ Manual schemas |
| **Auto-generated Models** | ❌ Manual | ❌ Manual | ✅ From schema |
| **Migration System** | ⚠️ Alembic (separate) | ⚠️ Alembic (separate) | ✅ Built-in |
| **DateTime Storage** | ✅ String format | ✅ String format | ⚠️ **Mixed (configurable)** |
| **Shared Table Compatibility** | ✅ Compatible | ✅ Compatible | ⚠️ **Depends on config** |
| **Maturity** | 🟢 Very Mature | 🟡 Growing | 🟡 Python client is new |
| **Community** | 🟢 Large | 🟡 Medium | 🟢 Large (TS/JS) |

### SQLAlchemy 2.0

**Best for**: Production applications requiring maximum control and flexibility

✅ **Strengths**:
- Battle-tested and mature (15+ years)
- Extremely flexible and powerful
- Full control over queries and relationships
- Supports field-level SELECT for query optimization
- Large ecosystem and community
- Comprehensive documentation
- Native async support in 2.0+

⚠️ **Considerations**:
- Requires separate Pydantic schemas for FastAPI
- More boilerplate compared to SQLModel
- Steeper learning curve
- Migration requires Alembic (separate tool)

**Code Example**:
```python
# Model definition (packages/sqlalchemy/src/my_sqlalchemy/models/user.py)
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    # ... more fields

# Optimized query (apps/api/src/routers/users.py)
result = await db.execute(
    select(User.id, User.username, User.created_at)  # Field-level SELECT
    .offset(skip).limit(limit)
)
```

### SQLModel

**Best for**: FastAPI applications prioritizing developer experience and rapid development

✅ **Strengths**:
- Single model definition for ORM + validation
- Automatic Pydantic model generation
- Inherits ALL SQLAlchemy capabilities (including field-level SELECT)
- Seamless FastAPI integration
- Less boilerplate code
- Type-safe with excellent IDE support
- Automatic table naming

⚠️ **Considerations**:
- Newer and less mature than SQLAlchemy
- Smaller ecosystem
- Explicit `__tablename__` causes Pylance type errors (use automatic naming)
- Still requires Alembic for migrations
- Some advanced SQLAlchemy patterns require wrapper code

**Code Example**:
```python
# Model definition (packages/sqlmodel/src/my_sqlmodel/models/user.py)
class User(SQLModel, table=True):  # Both ORM and Pydantic!
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    # ... more fields
    # Automatically generates Pydantic schema for FastAPI

# Same optimized query as SQLAlchemy
result = await db.execute(
    select(User.id, User.username, User.created_at)  # Field-level SELECT works!
    .offset(skip).limit(limit)
)
```

### Prisma Python

**Best for**: Projects prioritizing type safety and developer experience, willing to work within framework constraints

✅ **Strengths**:
- Auto-generated type-safe client from schema
- Built-in migration system (`prisma migrate`)
- Excellent TypeScript/JavaScript documentation
- Modern API design
- Strong type safety

✅ **Field-level SELECT via Partial Types**:

1. **Partial Types for Database-level Optimization** ✅ **Tested and Working**
   ```python
   # Step 1: Define partial type in prisma/partial_types.py (generation-time)
   from prisma.models import User

   UserMinimal = User.create_partial(
       "UserMinimal",
       include={"id", "username", "created_at"},
   )

   # Step 2: Generate client
   # $ prisma generate

   # Step 3: Use in queries (runtime)
   from prisma.partials import UserMinimal

   users = await UserMinimal.prisma(prisma).find_many()
   # Returns only selected fields from database
   ```

   **Important Notes**:
   - ✅ Field-level SELECT **IS supported** via Partial Types
   - ❌ Dynamic `select` parameter NOT supported (TypeScript feature only)
   - Partial types must be defined at generation time, not runtime
   - More verbose than SQLAlchemy but achieves same optimization

2. **DateTime Format Incompatibility**
   - Prisma stores datetime as Unix timestamp (integer): `1763295924173`
   - SQLAlchemy/SQLModel store as string: `"2025-11-16 12:25:24"`
   - **Result**: Cannot share same database table with other ORMs

3. **No Shared Table Support**
   - Prisma Python Client's datetime handling is incompatible
   - Attempting to mix Prisma with SQLAlchemy/SQLModel causes parsing errors
   - Must use separate tables or Prisma-only approach

**Why Prisma Cannot Be Used Alongside SQLAlchemy/SQLModel**:

```python
# Database table after mixed usage:
sqlite> SELECT id, username, created_at FROM user;
1|sqlalchemy_user|2025-11-16 12:25:24          # ✅ String format
2|sqlmodel_user|2025-11-16 12:25:24.160013     # ✅ String format
3|prisma_user|1763295924173                     # ❌ Unix timestamp!

# Result: All ORMs fail to parse mixed datetime formats
# SQLAlchemy/SQLModel: TypeError: fromisoformat: argument must be str
# Prisma: DataError: Conversion failed: input contains invalid characters
```

⚠️ **Additional Considerations**:
- Python client is less mature than TypeScript/JavaScript version
- Some Prisma features not available in Python (e.g., dynamic `select` parameter)
- Limited community resources for Python-specific issues
- Partial types require generation-time definition (less flexible than runtime queries)

### Recommendation

**For this project**: Use **SQLModel** for new FastAPI applications
- Combines best of SQLAlchemy (power) and Pydantic (validation)
- Less boilerplate than pure SQLAlchemy
- Full query optimization support (field-level SELECT)
- Compatible with SQLAlchemy for shared database usage
- Excellent FastAPI integration

**For production systems**: Use **SQLAlchemy 2.0**
- Maximum control and flexibility
- Battle-tested reliability
- Largest ecosystem and community support
- Full compatibility with other SQLAlchemy-based tools

**Consider Prisma Python carefully** for:
- Projects requiring dynamic query optimization (only static partial types supported)
- Projects needing to share tables with other ORMs (datetime compatibility issues)
- Applications where datetime precision matters
- Note: Python client has different feature set than TypeScript version

## 🔍 Key Learnings

### Monorepo Package Structure
All ORM packages (SQLAlchemy, SQLModel, Prisma) follow consistent `src` layout:
```
packages/{package-name}/
├── src/
│   └── my_{package-name}/    # Explicit namespace prevents conflicts
│       ├── __init__.py
│       └── ...
└── pyproject.toml            # packages = ["src"]
```

### SQLModel Benefits
**SQLModel** combines the best of SQLAlchemy and Pydantic:

✅ **Advantages**:
- Single model definition for both ORM and validation
- Automatic Pydantic model generation for FastAPI
- Inherits all SQLAlchemy capabilities (field-level SELECT, relationships, etc.)
- Type-safe with full IDE autocomplete support
- Automatic table naming (lowercase class name)
- Seamless FastAPI integration

⚠️ **Considerations**:
- Explicit `__tablename__` causes Pylance type errors (use automatic naming instead)
- Less mature ecosystem than SQLAlchemy
- Some SQLAlchemy patterns require wrapper code

### Detailed Prisma Python Client Analysis

For a comprehensive comparison of Prisma with SQLAlchemy and SQLModel, see the **ORM Comparison** section above.

**Summary of Key Features**:
1. ✅ Field-level SELECT supported via Partial Types (generation-time definition)
2. ❌ Dynamic `select` parameter NOT supported (TypeScript-only feature)
3. ⚠️ DateTime stored as Unix timestamp instead of string format (compatibility issue)
4. ⚠️ Cannot easily share database tables with SQLAlchemy/SQLModel due to datetime format
5. ⚠️ Python client has different feature set than TypeScript/JavaScript version

See detailed analysis in the [ORM Comparison section](#-orm-comparison-sqlalchemy-vs-sqlmodel-vs-prisma).

### Database Sharing and Compatibility

**SQLAlchemy + SQLModel**: ✅ **Fully Compatible**
- Both use the same `user` table seamlessly
- Datetime stored as string format (compatible)
- Can read and write each other's data without issues
- Shared database file at path specified by `DB_PATH` environment variable

**Prisma**: ❌ **Not Compatible with SQLAlchemy/SQLModel**
- Stores datetime as Unix timestamp (integer) instead of string
- Cannot share the same table - causes parsing errors in all ORMs
- Must use separate tables or Prisma-only approach
- See [ORM Comparison](#-orm-comparison-sqlalchemy-vs-sqlmodel-vs-prisma) for details

**Current Setup**:
- `DB_PATH` environment variable points to single SQLite database
- SQLAlchemy and SQLModel share the `user` table successfully
- Prisma endpoints exist but should not be used with shared tables

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
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/) - SQL databases in Python with simplicity
- [Prisma Documentation](https://www.prisma.io/docs) - Next-generation ORM
- [Pydantic Documentation](https://docs.pydantic.dev/) - Data validation library

### Testing
- [pytest Documentation](https://docs.pytest.org/) - Testing framework
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - Asyncio support for pytest
