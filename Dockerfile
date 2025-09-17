FROM python:3.11-slim

WORKDIR /app

# 安裝 poetry
RUN pip install --no-cache-dir poetry

# 複製 pyproject.toml & poetry.lock
COPY pyproject.toml poetry.lock* ./

# 安裝依賴
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 複製程式碼
COPY ./stage3/api/ /app/

# 啟動 FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
