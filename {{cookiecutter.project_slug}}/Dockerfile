FROM python:3.6-alpine

ARG APP_DIR=/app
WORKDIR "$APP_DIR"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . $APP_DIR/

ENTRYPOINT ["python", "-m", "aioworkers", "-c", "config.yaml", "-l", "info"]