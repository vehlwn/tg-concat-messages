FROM python:3.9.9-alpine
WORKDIR /app
COPY requirements.txt ./
RUN pip install --requirement requirements.txt --disable-pip-version-check --no-warn-script-location
COPY main.py app_settings.py ./
ENTRYPOINT python main.py
