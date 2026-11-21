# 1. Official lightweight Python runtime
FROM python:3.12-slim

# 2. Application working directory
WORKDIR /app

# 3. Dependency manifest (standard library only)
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# 4. Application code and startup
COPY taskboard/ ./taskboard/
RUN useradd --uid 10001 --create-home appuser \
    && mkdir -p /app/data \
    && chown -R appuser:appuser /app/data
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 TASKBOARD_DB=/app/data/tasks.db
USER 10001
EXPOSE 8080
CMD ["python", "-m", "taskboard.server"]
