FROM python:3.10-slim
LABEL authors="37525"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python -m app.init_db && uvicorn main:app --host 0.0.0.0 --port 8000"]
