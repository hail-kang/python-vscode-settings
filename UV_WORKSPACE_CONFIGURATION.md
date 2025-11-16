# UV Workspace for Unified Virtual Environment Management in Monorepo

## Overview

This document provides a detailed explanation of how to use **UV workspace** to enable all packages and apps in a monorepo to share **a single unified virtual environment (.venv)**.

> **Note**: For project overview and installation instructions, see [README.md](README.md). This document focuses on the **technical internals** and **pyproject.toml configuration** of UV workspace.

## What is UV Workspace?

UV workspace is a feature that allows multiple packages (workspace members) to be managed together within a single repository.

### Core Features

1. **Single Virtual Environment**: All workspace members share one `.venv`
2. **Unified Dependency Management**: All dependency versions managed with a single `uv.lock` file
3. **Editable Installation**: Cross-workspace member references are automatically installed in editable mode
4. **Unified Python Version**: All members use the same Python version range

### Traditional Approach vs UV Workspace

**Traditional Approach (Separate venvs)**:
```
apps/api/.venv/          (200MB)
packages/prisma/.venv/   (150MB)
packages/sqlalchemy/.venv/ (150MB)
packages/sqlmodel/.venv/ (150MB)
Total: 650MB + increased management complexity
```

**UV Workspace Approach**:
```
.venv/  (250MB)
Total: 250MB + centralized management
```

## Core Configuration

### 1. Root pyproject.toml - Workspace Definition

```toml
[tool.uv.workspace]
members = ["apps/*", "packages/*"]
```

**Explanation:**
- The `members` field specifies directory patterns to include in the workspace
- All projects under `apps/*` and `packages/*` are registered as workspace members
- This configuration causes all members to **share a single virtual environment**

### 2. Root pyproject.toml - Common Development Tools

```toml
[tool.uv]
dev-dependencies = [
    "ruff>=0.1.8",
    "pyright>=1.1.338",
]
```

**Explanation:**
- Dev-dependencies defined at the root apply to all workspace members
- Common development tools like linter (ruff) and type checker (pyright) are managed centrally
- No need for duplicate installation in each member

### 3. Package-level pyproject.toml - Basic Structure

**Example: packages/prisma/pyproject.toml**

```toml
[project]
name = "my-prisma"
version = "0.1.0"
description = "Shared Prisma models package"
requires-python = ">=3.10"

dependencies = [
    "prisma>=0.11.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]
```

**Explanation:**
- Each package has its own `pyproject.toml` but does not create a separate venv
- `requires-python` is handled as an intersection across the entire workspace (all use `>=3.10`)
- Each package's dependencies are installed together in the unified `.venv`

### 4. App-level pyproject.toml - Workspace Member References

**Example: apps/api/pyproject.toml**

```toml
[project]
name = "api"
version = "0.1.0"
description = "FastAPI application"
requires-python = ">=3.10"

dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "my-sqlalchemy",  # Internal workspace package
    "my-prisma",      # Internal workspace package
    "my-sqlmodel",    # Internal workspace package
]

[tool.uv.sources]
my-sqlalchemy = { workspace = true }
my-prisma = { workspace = true }
my-sqlmodel = { workspace = true }
```

**Key Configuration - `[tool.uv.sources]`:**

This section is **the core of workspace internal package references**:

- `{ workspace = true }`: Specifies that the dependency is a workspace member, not from PyPI
- UV uses this configuration to find packages in the `packages/` directory and **install them in editable mode**
- Thanks to editable installation, package code changes are reflected immediately (no reinstallation needed)

### 5. Development Dependency Groups

```toml
[dependency-groups]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.25.0",
]
```

**Explanation:**
- App-specific development dependencies are managed with `dependency-groups`
- Installed in the unified venv but logically grouped

## How the Unified Virtual Environment Works

### 1. Virtual Environment Creation and Initialization

```bash
# Run from project root
uv sync
```

**Internal Process:**
1. Creates a single virtual environment in the root `.venv/` directory
2. Analyzes all workspace members' `pyproject.toml` files
3. Collects all dependencies and locks versions in `uv.lock` file
4. Installs external packages normally, workspace members in editable mode

### 2. Dependency Resolution Process

```
1. UV discovers all workspace members
   └─ apps/api, packages/prisma, packages/sqlalchemy, packages/sqlmodel

2. Collects dependencies from each member
   ├─ fastapi>=0.104.0 (from apps/api)
   ├─ prisma>=0.11.0 (from packages/prisma)
   ├─ sqlalchemy>=2.0.0 (from packages/sqlalchemy)
   └─ sqlmodel>=0.0.22 (from packages/sqlmodel)

3. Detects workspace references
   └─ Checks { workspace = true } in [tool.uv.sources] section

4. Generates unified dependency graph
   └─ Resolves version conflicts and optimizes

5. Creates single uv.lock file
   └─ Pins exact versions for all packages

6. Batch installation to .venv
   ├─ External packages: Copied to site-packages/
   └─ Workspace members: Creates editable links
```

### 3. Benefits of Editable Installation

Since workspace members are installed in editable mode:

```python
# When you modify packages/prisma/src/models.py
# Changes are immediately reflected in apps/api

# No reinstallation needed!
from my_prisma.models import User  # Latest code available immediately
```

### 4. Python Version Management

```toml
# Set identically in all pyproject.toml files
requires-python = ">=3.10"
```

**Important:**
- Workspace uses the **intersection of all members' version requirements**
- If one member requires `>=3.11`, the entire workspace becomes `>=3.11`
- The actual version used is recorded in `.venv/pyvenv.cfg`

```
# .venv/pyvenv.cfg
version_info = 3.10.14
```

## UV Command Usage

### Sync Entire Workspace

```bash
# Install dependencies for all members
uv sync

# Include development dependencies
uv sync --all-extras
```

### Work with Specific Packages

```bash
# Run script for specific package
uv run --package api python -m uvicorn src.main:app

# Run tests for specific package
uv run --package api pytest
```

### Add Dependencies

```bash
# Add new dependency to API app
cd apps/api
uv add httpx

# Reflected across entire workspace (uv.lock updated)
```

### Update Dependencies

```bash
# Update all workspace dependencies
uv lock --upgrade

# Update specific package only
uv lock --upgrade-package fastapi
```

## Benefits of Unified Configuration

### ✅ 1. Prevents Dependency Conflicts

All packages use the same library versions, eliminating version mismatch issues

```toml
# If both prisma and sqlalchemy use pydantic
# UV automatically selects one compatible version
```

### ✅ 2. Disk Space Savings (60%+)

- Separate venvs: 650MB (many duplicates)
- Unified venv: 250MB (deduplication)
- **Savings: 400MB (61.5%)**

### ✅ 3. Faster Installation Time

- Common dependencies (pydantic, fastapi, etc.) installed only once
- Workspace members create symbolic links only (instant completion)

### ✅ 4. Consistent Development Environment

- All developers use the same `uv.lock` file
- Exact same environment reproducible in CI/CD

### ✅ 5. Real-time Code Reflection

Thanks to editable installation:
```bash
# Modify code in packages/
# → Immediately available in apps/
# → No reinstallation/rebuild needed
```

## Additional Integrated Configurations

### Ruff Integration

Unified linting/formatting rules for entire monorepo in root `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py310"
line-length = 100
src = ["apps/*/src", "packages/*/src"]  # Recognizes all source directories

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "ANN", ...]  # Rules applied to all
```

**Benefits:**
- Same code style applied to all workspace members
- Eliminates duplicate configuration
- Maintains consistent code quality

### Pyright/Pylance Integration

Workspace-wide type checking configuration in `pyrightconfig.json`:

```json
{
  "executionEnvironments": [
    {
      "root": "apps/api",
      "extraPaths": ["packages/sqlalchemy/src", "packages/prisma/src", "packages/sqlmodel/src"]
    }
  ]
}
```

**Benefits:**
- Type inference support across workspace members
- Automatic import path recognition
- Perfect autocomplete in VSCode

## Caveats and Limitations

### ⚠️ When Dependencies Conflict

If different members require incompatible versions:

```toml
# apps/api/pyproject.toml
dependencies = ["pydantic>=2.0"]

# packages/legacy/pyproject.toml
dependencies = ["pydantic<2.0"]
```

**Solutions:**
1. **Recommended**: Update all members to compatible versions
2. **Alternative**: Exclude from workspace and use path dependency

### ⚠️ Python Version Mismatch

```toml
# One member uses 3.11+ features
requires-python = ">=3.11"

# Another member supports 3.10
requires-python = ">=3.10"

# Result: Entire workspace constrained to >=3.11
```

### ⚠️ When Workspace is Not Suitable

Consider using separate venvs instead of workspace for:

- Completely independent projects simply coexisting
- Different Python version requirements
- Cases where dependency isolation is critical

## Migration Guide

### Transitioning from Separate venvs to Workspace

1. **Remove existing venvs**
   ```bash
   rm -rf apps/*/venv packages/*/venv
   ```

2. **Create root pyproject.toml**
   ```toml
   [tool.uv.workspace]
   members = ["apps/*", "packages/*"]
   ```

3. **Add workspace reference configuration**
   Add `[tool.uv.sources]` section to each app's `pyproject.toml`

4. **Unified installation**
   ```bash
   uv sync
   ```

### Verification

```bash
# Verify virtual environment exists only at root
ls -la .venv/

# Verify workspace members are installed as editable
uv pip list | grep "my-"

# Expected output:
# my-prisma        0.1.0  /path/to/packages/prisma
# my-sqlalchemy    0.1.0  /path/to/packages/sqlalchemy
# my-sqlmodel      0.1.0  /path/to/packages/sqlmodel
```

## Summary

This project implements unified virtual environment management through these key configurations:

1. **`[tool.uv.workspace]`**: Defines workspace members
2. **`[tool.uv.sources]`**: References internal workspace packages (`{ workspace = true }`)
3. **Single `.venv/`**: All dependencies installed in one virtual environment
4. **Editable installation**: Real-time code reflection across workspace members
5. **Unified `uv.lock`**: Consistent dependency version management

This approach provides the combined benefits of **preventing dependency conflicts**, **disk space savings**, **faster installation**, **consistent environments**, and **real-time development**.
