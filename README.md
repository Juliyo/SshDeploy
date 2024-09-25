# SshKeyDeploy

A CLI tool to create and deploy SSH keys

# Usage

```bash
SshKeyDeploy [-h]
```

# Development

## Prerequisites

```bash
python3 -m pip install --upgrade build
```

```bash
python3 -m pip install --upgrade twine
```

## Build package

```bash
python3 -m build
```

## Upload package

```bash
python3 -m twine upload dist/*
```
