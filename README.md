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
├── .vscode/              # VSCode configuration (settings, extensions, tasks)
├── apps/                 # Applications
│   └── api/             # FastAPI application
│       ├── src/         # API source code
│       ├── tests/       # API tests
│       ├── pyproject.toml
│       └── .python-version
├── packages/            # Shared packages (future)
├── pyproject.toml       # Workspace configuration
├── .python-version      # Python version
├── uv.lock              # Dependency lock file (generated)
├── pyrightconfig.json   # Pyright configuration
└── README.md           # This file
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

4. **Open in VSCode**
```bash
code .
```

## ⚙️ Configuration Goals

### VSCode Settings
The `.vscode/settings.json` will be optimized for:
- Automatic formatting on save using ruff
- Real-time type checking with pyright
- Intelligent code completion
- Import organization
- Path resolution for project structure

### Ruff Configuration
Testing and documenting:
- Linting rules and severity levels
- Formatting preferences
- Integration with VSCode
- Performance benchmarks

### Pyright Configuration
Validating:
- Type checking strictness levels
- Import resolution strategies
- Integration with FastAPI and SQLAlchemy types
- Performance and accuracy

## 📝 Development Workflow

1. **Phase 1**: Basic setup and tool configuration
2. **Phase 2**: FastAPI application with SQLAlchemy
3. **Phase 3**: Prisma integration and comparison
4. **Phase 4**: Documentation of optimal settings

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
