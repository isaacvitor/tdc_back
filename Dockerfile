FROM python:3.7-slim
ENV TDC_DATABASE_PATH=./data/db.sql
ENV TDC_MAX_AGENTS=10
ENV TDC_MAX_CLIENTS=100
ARG TDC_TZ='Europe/Lisbon'
ENV DEFAULT_TZ ${TDC_TZ}
RUN ln -snf /usr/share/zoneinfo/$DEFAULT_TZ /etc/localtime && echo $DEFAULT_TZ > /etc/timezone
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /usr/src/app
COPY . .
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
