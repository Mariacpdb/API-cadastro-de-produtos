# Utiliza uma imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia todos os arquivos da sua aplicação para o container
COPY . .

# Instala dependências (nesse projeto não tem dependência extra)
# Então não precisa instalar nada além do próprio Python

# Comando para rodar a aplicação automaticamente
CMD ["python", "app.py"]
