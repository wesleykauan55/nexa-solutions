FROM python:3.12-slim

# Evita a criação de arquivos .pyc e força a saída no console
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependências do sistema necessárias para o Postgres
RUN apt-get update && apt-get install -y libpq-dev gcc

# Instala dependências do Python
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY backend/ /app/

# Expõe a porta do Django
EXPOSE 8000

# Executa migrações e sobe o servidor
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"