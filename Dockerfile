FROM python:latest

ENV SRC_DIR /usr/bin/spotiplex/
COPY ./spotiplex ${SRC_DIR}/
WORKDIR ${SRC_DIR}

ENV PYTHONUNBUFFERED=1

RUN pip install -r requirements.txt
CMD ["python", "main.py"]