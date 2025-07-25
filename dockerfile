FROM python:3.11-slim

# Install uv
RUN pip install --no-cache-dir uv

# Set workdir
WORKDIR /app

# Copy project metadata
COPY pyproject.toml ./

# Install dependencies
RUN uv venv && \
    . .venv/bin/activate && \
    uv pip install -r pyproject.toml

# Copy everything else
COPY . .

# Entrypoint
CMD ["uv","run", "main.py"]
