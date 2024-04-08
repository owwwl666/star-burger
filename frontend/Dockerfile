FROM node:16.16.0-alpine as node
WORKDIR /frontend
COPY /frontend/ .
RUN npm ci --include=dev
