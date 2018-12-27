FROM python:3

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . /code

WORKDIR /code/web_engine

CMD python app.py
