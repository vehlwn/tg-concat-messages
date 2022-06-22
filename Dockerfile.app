FROM python:3.9.5-alpine

WORKDIR /home/app
RUN adduser -D app
USER app:app

COPY --chown=app:app requirements.txt ./
RUN pip install -r requirements.txt --disable-pip-version-check --no-warn-script-location --user

COPY --chown=app:app main.py app_settings.py config.ini client.session ./
ENTRYPOINT python main.py
