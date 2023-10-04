FROM python:3.9

WORKDIR /app

COPY event-generator.py /app

RUN pip install kubernetes

CMD ["python", "event-generator.py"]
