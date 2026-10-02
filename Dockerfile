FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir . && useradd --uid 10001 --create-home jevlens && mkdir /app/data && chown jevlens:jevlens /app/data
USER jevlens
ENV JEVLENS_DATA_DIR=/app/data
EXPOSE 8787
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8787/health')"
CMD ["uvicorn", "jevlens.app:create_app", "--factory", "--host", "0.0.0.0", "--port", "8787"]
