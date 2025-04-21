FROM python:3.8-slim


WORKDIR /app

# Install system dependencies in a single step (reduces image size)
RUN apt-get update && apt-get install -y \
    gcc libc-dev build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir --default-timeout=100 && \
    pip install redis --no-cache-dir --default-timeout=100


COPY . .

EXPOSE 8000

CMD ["sh", "-c", "echo 'Running migrations...' && python manage.py migrate && echo 'Starting Django server...' && exec python manage.py runserver 0.0.0.0:8000"]

