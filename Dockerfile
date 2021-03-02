FROM python:alpine3.13

RUN pip install pika

COPY python_processor.py /processor/
COPY util/*.py /processor/util/

ENTRYPOINT ["python", "/processor/python_processor.py", "$@", "--"]