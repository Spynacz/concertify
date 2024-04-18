FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend
COPY ./requirements.txt /backend/
COPY ./entrypoint.sh /backend/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /backend/
