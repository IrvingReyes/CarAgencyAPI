FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini .
COPY alembic ./alembic
COPY app ./app

EXPOSE 8000

# Apply migrations, load sample data (only on an empty table) and start the API
CMD ["sh", "-c", "alembic upgrade head && python -m app.seed && fastapi run app/main.py --host 0.0.0.0 --port 8000"]
