FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "uvicorn", "edutracker.main:app", "--host", "0.0.0.0", "--port", "8000"]