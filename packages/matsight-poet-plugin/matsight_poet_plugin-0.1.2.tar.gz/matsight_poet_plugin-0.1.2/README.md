# Poet Plugin
A Poetry plugin to enable exclusivity between groups.  
Poet stands for **Po**etry **E**xclusivity **T**oggle (or some other excuse, I did not want a verbose package name and
`poet` seemed short and sweet since this plugin changes the internal poetry package during runtime).

## Installation
### In a clean project
When starting with a clean `pyproject.toml`, before any such cross-group non-exclusive dependencies are defined,
simply install with `poetry add poet-plugin` or `poetry self add poet-plugin`.

### In a cross-dependency project
In cases where the `pyproject.toml` already has a complicated structure that would cause the poetry CLI to fail,
such as CICD pipelines, install via `pip` first:
```shell
poetry shell
pip install poet-plugin
```

## Usage
When running `poetry install`, the various options (`--only`, `--without`) are parsed to ensure the dependency resolver 
only considers what needs to be considered.  
This allows a non-mutually exclusive group definition, so that e.g. the `dev` group can refer to
some local path, whereas a `prod` group refers to git URI.  

### Examples
Considering the following `pyproject.toml`, depicting a mono-repository:
```
[tool.poetry.dependencies]
python = ">=3.8,<3.12"
poetry = "^1.2.0"

[tool.poetry.group.prod.dependencies]
foo = {git = "https://github.com/bar/foo", subdirectory = "src/libs/foo"}

[tool.poetry.group.dev.dependencies]
foo = {path = "../../libs/foo", develop = true}
```
- Install the prod version:
  - `poetry install --without dev`, OR
  - `poetry install --only prod`
- Install the dev version:
  - `poetry install --without prod`, OR
  - `poetry install --only dev`
