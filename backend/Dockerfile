FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /star_burger
COPY /backend/ .
COPY /media .
RUN chmod +x ./ -R
RUN python -m pip install --upgrade pip  \
    && pip install -r requirements.txt  \
    && apk add postgresql-dev gcc python3-dev musl-dev


