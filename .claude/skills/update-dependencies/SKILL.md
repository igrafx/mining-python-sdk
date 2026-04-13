---
name: update-dependencies
description: Update SDK dependencies to latest compatible versions while ensuring KNIME connector compatibility
user_invocable: true
---

# Update SDK Dependencies

Update all dependencies in `pyproject.toml` to their latest versions that are compatible with the KNIME Mining connector's `pixi.toml`.

## Step 1: Read current state

1. Read the SDK's `pyproject.toml` in the repo root to get current dependency versions.
2. Fetch the KNIME connector's `pixi.toml` from GitHub to get KNIME-side constraints:
   - URL: `https://raw.githubusercontent.com/igrafx/KNIME-Mining-connector/dev/pixi.toml`
   - Use `WebFetch` to retrieve and parse its contents.

## Step 2: Parse pixi.toml constraints

Extract version ranges dynamically from pixi.toml — do NOT hardcode any versions. Parse:
- `[dependencies]` section (conda dependencies shared across all platforms)
- `[pypi-dependencies]` section
- All `[target.<platform>.dependencies]` sections (win-64, linux-64, osx-64, osx-arm64)

For each dependency, determine the **effective constraint** by combining all sections where it appears. A dependency pinned in conda (e.g., `pandas = ">=2.0.3,<2.1.0"`) takes precedence because pixi resolves conda first and pypi cannot override it.

Key dependencies to track: `pandas`, `numpy`, `urllib3`, `requests`, `networkx`, `sqlalchemy`, `python-dotenv`, `toml`, `pydruid`, `python`.

## Step 3: Check PyPI for latest versions

For each dependency in `pyproject.toml` under `[tool.poetry.dependencies]`:
- Query PyPI JSON API: `https://pypi.org/pypi/<package>/json`
- Get the latest stable version (ignore pre-releases)

## Step 4: Cross-check KNIME compatibility

For each SDK dependency that also appears in pixi.toml:
1. Check if the **latest PyPI version** falls within pixi.toml's constraint range.
2. If compatible: propose updating to the latest version.
3. If **incompatible**: flag the conflict and determine the latest version that IS compatible with pixi.toml's range. Propose that version instead.
4. For the Python version: ensure the SDK's `python` constraint is satisfiable alongside pixi.toml's Python constraint.

**Important**: `knime-python-base` (a conda package on the KNIME channel) hard-pins several transitive dependencies like `pandas` to exact versions. The pixi.toml conda constraints reflect these hard pins. SDK dependency ranges MUST accept these pinned versions.

## Step 5: Report findings

Present the user with a table showing:

```
| Dependency     | Current (SDK) | Latest (PyPI) | pixi.toml constraint     | Proposed | Notes          |
|----------------|---------------|---------------|--------------------------|----------|----------------|
| pandas         | >=2.0.3,<4    | 3.x.x         | >=2.0.3,<2.1.0 (conda)  | >=2.0.3,<4 | Latest incompatible with KNIME |
| ...            | ...           | ...           | ...                      | ...      | ...            |
```

Highlight any conflicts or cases where the latest version cannot be used.

Wait for user confirmation before proceeding to Step 6.

## Step 6: Apply updates

After user confirms the proposed versions, update `pyproject.toml` with the approved dependency versions.

## Step 7: Validate

Run the following commands sequentially in the SDK repo root:

```bash
poetry lock
```
If `poetry lock` fails, diagnose the issue (version conflict, missing package, etc.), fix the constraint in `pyproject.toml`, and retry.

```bash
poetry install
```
If `poetry install` fails, diagnose and fix.

```bash
pytest
```
Report test results to the user. If tests fail, investigate whether the failures are related to the dependency changes.
