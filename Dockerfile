FROM python:3.8.1 as dev

RUN pip install poetry==1.0.0
ENV PATH="/root/.poetry/bin:${PATH}"

WORKDIR /app/

ADD . /app
RUN poetry install

CMD poetry run python /app/authenticator/app.py
