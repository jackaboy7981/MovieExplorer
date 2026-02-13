FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir uv==0.10.2

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

RUN pip install pylint && pylint app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
