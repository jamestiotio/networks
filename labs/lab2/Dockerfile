FROM tiangolo/uvicorn-gunicorn:python3.9
COPY ./app /app

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
COPY ./app /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN apt-get update && apt-get install -y fortune
