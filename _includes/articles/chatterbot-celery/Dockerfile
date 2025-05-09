FROM python:3.11-slim-bookworm

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r /code/requirements.txt
RUN python -m spacy download en_core_web_sm

COPY ./tasks.py /code

WORKDIR /code

CMD ["celery", "-A", "tasks", "worker", "--loglevel=INFO"]
