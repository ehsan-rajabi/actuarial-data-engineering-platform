FROM python:3.14-slim

WORKDIR /app

# Install system dependencies and Microsoft ODBC Driver 18
RUN apt-get update \
    && apt-get install -y curl gnupg2 apt-transport-https ca-certificates unixodbc-dev \
    && curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl -sSL https://packages.microsoft.com/config/debian/12/prod.list \
        -o /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "actuarial_platform.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]