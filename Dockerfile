FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY flask_s3_app.py .

EXPOSE 5000
CMD ["python", "flask_s3_app.py"]
