FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY seed_tables_data.py .

CMD ["python", "seed_tables_data.py"]