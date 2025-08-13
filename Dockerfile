FROM python:3.13-alpine

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1


WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    build-base \
    python3-dev \
    mariadb-dev \
    libffi-dev \
    jpeg-dev \
    zlib-dev \
    tzdata \
    bash \
    curl \
    git

# Copy the rest of the code
COPY . .

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Install dependencies
RUN poetry install --no-root

# Expose the port
EXPOSE 6060


# Run using Uvicorn
RUN chmod +x start.sh
CMD ["./start.sh"] 
