FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir -e ".[web,all-providers]" \
    && adduser --disabled-password --home /data/coach appuser \
    && mkdir -p /data/coach && chown appuser /data/coach

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')"

CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8000"]
