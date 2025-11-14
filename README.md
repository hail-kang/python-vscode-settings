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
- **SQLAlchemy**: SQL toolkit and ORM
- **Prisma** (planned): Next-generation ORM

## 📁 Project Structure (Monorepo)

```
python-vscode-settings/
├── .vscode/                                 # VSCode configuration (git ignored)
│   ├── settings.json                        # Editor settings
│   └── extensions.json                      # Recommended extensions
├── .vscode.example/                         # Example VSCode configuration
│   ├── settings.json                        # Example settings
│   └── extensions.json                      # Example extensions
├── apps/                                    # Applications
│   └── api/                                 # FastAPI application
│       ├── src/                             # API source code
│       ├── tests/                           # API tests
│       ├── pyproject.toml                   # App dependencies
│       └── .python-version                  # Python 3.10.14
├── packages/                                # Shared packages
│   └── db/                                  # Database models package
│       ├── src/
│       │   └── models/                      # SQLAlchemy models
│       │       ├── __init__.py
│       │       ├── base.py                  # Base declarative class
│       │       └── user.py                  # User model
│       └── pyproject.toml                   # SQLAlchemy dependency
├── pyproject.toml                           # Workspace & ruff configuration
├── pyrightconfig.json                       # Pyright type checking config
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

2. **Phase 2**: Shared packages and models ✅
   - `packages/db` with SQLAlchemy models
   - User model with type-safe mappings

3. **Phase 3**: FastAPI application (In Progress)
   - API endpoints and routing
   - Database integration
   - Testing setup

4. **Phase 4**: Prisma integration and comparison (Planned)
5. **Phase 5**: Documentation of optimal settings (Planned)

## 🧪 Testing Strategy

- Unit tests for utility functions
- Integration tests for API endpoints
- Type checking validation
- Linting rule effectiveness

## 📚 Documentation

Documentation will cover:
- VSCode extension recommendations
- Recommended settings.json configuration
- Tool-specific configurations
- Common issues and solutions
- Performance comparisons

## 🤝 Contributing

This is a validation project. Feedback on configurations and best practices is welcome.

## 📄 License

MIT License

## 🔗 Resources

- [uv Documentation](https://github.com/astral-sh/uv)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [pyright Documentation](https://github.com/microsoft/pyright)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
