# Kontext AI

Kontext AI is an AI empowered tool for data analytics that runs on your local computer.

## Development

This section shows you how to setup local environment to participate in development of kontext-ai.

### Setup Python environment 

Create virtual environment. Please use **Python 3.9**.

```
python -m venv .venv
```

Activate the virtual environment.

For Windows:
```
.\.venv\Scripts\activate
```

For UNIX-alike systems:
```
source ./.venv/bin/activate
```

Upgrade `pip`:
```
python.exe -m pip install --upgrade pip
```

Install poetry:
```
pip install poetry
```

Refer to [https://python-poetry.org/docs/](https://python-poetry.org/docs/) for details about Poetry.

Install packages:
```
poetry install
```

### Build package

```
poetry build
```

### Upload to PyPi

```
poetry publish
```

