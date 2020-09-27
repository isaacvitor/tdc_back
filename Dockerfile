FROM python:3.7-alpine
ENV TDC_DATABASE_PATH=./data/db.sql
ENV TDC_MAX_AGENTS=10
ENV TDC_MAX_CLIENTS=100
RUN apk add --no-cache git && apk add -U tzdata
RUN cp /usr/share/zoneinfo/Europe/Portugal /etc/localtime
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "uvicorn", "main:app" ]
EXPOSE 8000