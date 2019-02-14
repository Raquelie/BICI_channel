FROM python:3.6-alpine

COPY requirements.txt /

RUN pip install -r /requirements.txt

ADD *.py /

ENTRYPOINT ["python", "bot.py"]