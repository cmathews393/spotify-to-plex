FROM python:latest

ENV SRC_DIR /usr/bin/spotiplex/
COPY ./current-version ${SRC_DIR}/
WORKDIR ${SRC_DIR}

ENV PYTHONUNBUFFERED=1

RUN pip install -r requirements.txt
CMD ["python", "./spotiplex/main.py"]