FROM node:16.16.0-alpine as node
WORKDIR /app
COPY ./bundles-src ./bundles-src
COPY ./package-lock.json .
COPY ./package.json .
RUN npm ci --include=dev
RUN /app/node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="/app"

FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /star_burger
COPY . .
RUN mkdir "bundles"
COPY --from=node /app/bundles ./bundles
RUN python3 -m pip install --upgrade pip  \
    && pip install -r requirements.txt  \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && python manage.py collectstatic --noinput


