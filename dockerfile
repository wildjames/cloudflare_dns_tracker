FROM python:3.10.7-slim-buster

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# Define environment variables for credentials
ENV CLOUDFLARE_ZONE=""
ENV CLOUDFLARE_DOMAIN_ID=""
ENV GMAIL_USER=""
ENV GMAIL_PASS=""
ENV GMAIL_SEND_TO=""

CMD ["python", "main.py"]