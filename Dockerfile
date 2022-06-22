FROM python:3.10.1-alpine3.15
WORKDIR /app
COPY requirements.txt ./
RUN pip install --requirement requirements.txt --disable-pip-version-check \
    --no-warn-script-location --user
COPY main.py app_settings.py ./
ENTRYPOINT python main.py
