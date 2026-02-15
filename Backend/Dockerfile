FROM python:3.14-slim

WORKDIR /app

RUN pip install --no-cache-dir uv==0.10.2

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .
RUN chmod +x app/scripts/startup.sh

EXPOSE 8000

CMD ["app/scripts/startup.sh"]
