FROM python:latest

ENV SRC_DIR /usr/bin/spotiplex/
COPY ./current-version ${SRC_DIR}/
WORKDIR ${SRC_DIR}

ENV PYTHONUNBUFFERED=1

RUN pip install plexapi spotipy python-decouple
CMD ["python", "main.py"]