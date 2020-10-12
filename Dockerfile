FROM python:3.9-slim

RUN groupadd pygroup && useradd -m -g pygroup -s /bin/bash pyuser
RUN mkdir -p /home/pyuser/app

COPY . /home/pyuser/app
WORKDIR /home/pyuser/app
RUN apt-get update && apt-get install -y python3-dev libmariadbclient-dev
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /home/pyuser/app/app/requirements.txt
RUN chown -R pyuser:pygroup /home/pyuser

USER pyuser

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
