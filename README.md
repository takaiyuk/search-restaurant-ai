# search-restaurant-ai

## Quick start

1. Install poetry

- https://python-poetry.org/docs/#installing-with-the-official-installer

2. Install dependencies

```sh
poetry install
```

3. Set secret keys

```sh
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit .streamlit/secrets.toml
```

4. Run the app

```sh
poetry run invoke run
```

5. Open the app

- Local URL: http://localhost:8501

6. Ask a question

- Type a question in the input box and press Enter
