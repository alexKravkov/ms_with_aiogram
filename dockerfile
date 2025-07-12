FROM python:3.11-slim

# Install uv
RUN pip install --no-cache-dir uv

# Set workdir
WORKDIR /app

# Copy project metadata
COPY pyproject.toml ./
COPY uv.lock ./

# Install dependencies
RUN if [ -f "uv.lock" ]; then uv venv && uv pip install -r uv.lock; else uv pip install -r pyproject.toml; fi

# Copy everything else
COPY . .

# Entrypoint
CMD ["python", "main.py"]
