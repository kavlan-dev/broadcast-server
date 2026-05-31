FROM python:slim
WORKDIR /app

RUN pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml README.md ./
COPY src/ src/

RUN poetry install

CMD ["poetry", "run", "broadcast-server", "start", "--host", "0.0.0.0"]