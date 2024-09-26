# SshKeyDeploy

A CLI tool to create and deploy SSH keys

# Usage

```bash
SshKeyDeploy [-h]
```

# Development

## Prerequisites

```bash
python -m pip install --upgrade build
```

```bash
python -m pip install --upgrade twine
```

## Build package

```bash
python -m build
```

## Upload package

```bash
python -m twine upload dist/*
```
