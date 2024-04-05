FROM node:16.16.0-alpine as node
WORKDIR /app
COPY frontend/ .
RUN npm ci --include=dev
RUN ./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /star_burger
COPY . .
RUN mkdir "frontend/bundles"
COPY --from=node /app/bundles /frontend/bundles
RUN chmod +x ./ -R
RUN python -m pip install --upgrade pip  \
    && pip install -r backend/requirements.txt  \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && python backend/manage.py collectstatic --noinput


