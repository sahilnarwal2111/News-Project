FROM python:3.8.17-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .
CMD ["python3", "app.py"]